from __future__ import annotations

import json
import random
import time
import uuid
import warnings
from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import Depends, FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload
from starlette.middleware.sessions import SessionMiddleware

from .auth import configured_providers, dev_login, login_redirect, oauth_callback, public_user, require_user
from .content_loader import seed_course_if_empty
from .database import SessionLocal, create_all, get_db
from .models import AnswerChoice, DiagnosticResult, ExamSession, FlashcardProgress, Lesson, LessonProgress, MistakeBank, Module, Question, QuizAnswer, QuizAttempt, Term
from .ratelimit import rate_limit
from .settings import settings
from .tutor import ask_coverage_coach, call_ollama_raw  # noqa: F401 used in study_plan

FRONTEND_DIR = __import__("pathlib").Path(__file__).resolve().parent.parent / "frontend"


class LessonProgressIn(BaseModel):
    completed: bool = True
    confidence: int = Field(default=0, ge=0, le=3)
    notes: str = Field(default="", max_length=5000)
    saved_for_review: bool = False


class QuizSubmitIn(BaseModel):
    mode: str = Field(default="practice", max_length=50)
    answers: dict[int, int] = Field(default_factory=dict, description="question_id -> selected_choice_id")


class TutorAskIn(BaseModel):
    message: str = Field(min_length=2, max_length=1200)


class DiagnosticSubmitIn(BaseModel):
    answers: dict[int, int] = Field(default_factory=dict, description="question_id -> selected_choice_id")


class FlashcardReviewIn(BaseModel):
    rating: int = Field(ge=1, le=4)


class ExamSubmitIn(BaseModel):
    answers: dict[int, int] = Field(default_factory=dict, description="question_id -> choice_id")


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_all()
    db = SessionLocal()
    try:
        seed_course_if_empty(db)
    finally:
        db.close()
    if settings.enable_dev_login and "localhost" not in settings.app_base_url:
        warnings.warn("WARNING: ENABLE_DEV_LOGIN=true on a non-localhost URL. Disable before launch!")
    yield


_docs_url = "/docs" if settings.enable_dev_login else None
_redoc_url = "/redoc" if settings.enable_dev_login else None
app = FastAPI(title="P&C License Prep Academy API", version="2.1.0", lifespan=lifespan,
              docs_url=_docs_url, redoc_url=_redoc_url)

origins = settings.cors_origin_list if settings.enable_dev_login else [settings.app_base_url]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False if origins == ["*"] else True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SessionMiddleware, secret_key=settings.session_secret, same_site="lax", https_only=settings.app_base_url.startswith("https"))


@app.middleware("http")
async def security_headers(request: Request, call_next: Any) -> Any:
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    if not settings.enable_dev_login:
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response

if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")


def module_out(module: Module) -> dict[str, Any]:
    return {
        "id": module.id,
        "slug": module.slug,
        "title": module.title,
        "description": module.description,
        "sort_order": module.sort_order,
        "lesson_count": len(module.lessons),
    }


def lesson_out(lesson: Lesson) -> dict[str, Any]:
    return {
        "id": lesson.id,
        "slug": lesson.slug,
        "module_id": lesson.module_id,
        "title": lesson.title,
        "summary": lesson.summary,
        "body": lesson.body,
        "example": lesson.example,
        "memory_tip": lesson.memory_tip,
        "audio_script": lesson.audio_script,
        "estimated_minutes": lesson.estimated_minutes,
        "sort_order": lesson.sort_order,
    }


def question_out(question: Question, include_answer: bool = False) -> dict[str, Any]:
    data = {
        "id": question.id,
        "module_id": question.module_id,
        "lesson_id": question.lesson_id,
        "question_text": question.question_text,
        "question_type": question.question_type,
        "difficulty": question.difficulty,
        "choices": [
            {
                "id": c.id,
                "choice_text": c.choice_text,
                "explanation": c.explanation if include_answer else "",
                "sort_order": c.sort_order,
                **({"is_correct": c.is_correct} if include_answer else {}),
            }
            for c in question.choices
        ],
        "explanation": question.explanation if include_answer else "",
    }
    return data


@app.get("/")
def home():
    index = FRONTEND_DIR / "index.html"
    if index.exists():
        return FileResponse(str(index))
    return {"ok": True, "app": settings.app_name}


@app.get("/api/health")
def health(db: Session = Depends(get_db)):
    return {
        "ok": True,
        "version": "2.1.0",
        "modules": db.scalar(select(func.count()).select_from(Module)),
        "lessons": db.scalar(select(func.count()).select_from(Lesson)),
        "questions": db.scalar(select(func.count()).select_from(Question)),
        "providers": configured_providers(),
        "free_public_access": True,
        "coverage_coach_mode": settings.tutor_mode,
    }


@app.get("/auth/providers")
def auth_providers():
    return {"providers": configured_providers(), "dev_login_enabled": settings.enable_dev_login}


@app.get("/auth/login/{provider}")
async def login(provider: str, request: Request):
    return await login_redirect(request, provider)


@app.get("/auth/callback/{provider}")
async def callback(provider: str, request: Request, db: Session = Depends(get_db)):
    return await oauth_callback(request, db, provider)


@app.get("/auth/dev-login")
def dev(request: Request, db: Session = Depends(get_db)):
    return dev_login(request, db)


@app.post("/auth/logout")
def logout(request: Request):
    request.session.clear()
    return {"ok": True}


@app.get("/api/me")
def me(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    if not user_id:
        return {"user": None}
    user = db.get(__import__("app.models", fromlist=["User"]).User, int(user_id))
    return {"user": public_user(user) if user else None}


@app.get("/api/modules")
def list_modules(db: Session = Depends(get_db)):
    modules = db.scalars(select(Module).options(selectinload(Module.lessons)).where(Module.is_active == True).order_by(Module.sort_order, Module.id)).all()
    return [module_out(m) for m in modules]


@app.get("/api/modules/{slug}")
def get_module(slug: str, db: Session = Depends(get_db)):
    module = db.scalar(select(Module).options(selectinload(Module.lessons)).where(Module.slug == slug, Module.is_active == True))
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    return {**module_out(module), "lessons": [lesson_out(l) for l in module.lessons if l.is_active]}


@app.get("/api/lessons/{slug}")
def get_lesson(slug: str, db: Session = Depends(get_db)):
    lesson = db.scalar(select(Lesson).where(Lesson.slug == slug, Lesson.is_active == True))
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    terms = db.scalars(select(Term).where(Term.module_id == lesson.module_id).order_by(Term.term)).all()
    module = db.scalar(select(Module).where(Module.id == lesson.module_id))
    return {
        **lesson_out(lesson),
        "module_slug": module.slug if module else "",
        "module_title": module.title if module else "",
        "terms": [term_out(t) for t in terms],
    }


def term_out(term: Term) -> dict[str, Any]:
    return {
        "id": term.id,
        "module_id": term.module_id,
        "lesson_id": term.lesson_id,
        "term": term.term,
        "plain_english_definition": term.plain_english_definition,
        "exam_definition": term.exam_definition,
        "example": term.example,
    }


@app.get("/api/terms")
def list_terms(module_slug: str | None = None, db: Session = Depends(get_db)):
    stmt = select(Term).order_by(Term.term)
    if module_slug:
        stmt = stmt.join(Module).where(Module.slug == module_slug)
    return [term_out(t) for t in db.scalars(stmt).all()]


@app.get("/api/questions")
def list_questions(module_slug: str | None = None, limit: int = Query(10, ge=1, le=50), db: Session = Depends(get_db)):
    stmt = select(Question).options(selectinload(Question.choices)).where(Question.is_active == True)
    if module_slug:
        stmt = stmt.join(Module).where(Module.slug == module_slug)
    questions = list(db.scalars(stmt).all())
    random.shuffle(questions)
    return [question_out(q) for q in questions[:limit]]


@app.post("/api/quiz/submit")
def submit_quiz(payload: QuizSubmitIn, request: Request, db: Session = Depends(get_db)):
    user = require_user(request, db)
    rate_limit(f"quiz:{user.id}", 20, 60)
    if len(payload.answers) > 50:
        raise HTTPException(status_code=400, detail="Submit 50 answers or fewer at a time")

    attempt = QuizAttempt(user_id=user.id, mode=payload.mode, total_questions=len(payload.answers))
    db.add(attempt)
    db.flush()

    correct_count = 0
    results = []
    for question_id, choice_id in payload.answers.items():
        question = db.scalar(select(Question).options(selectinload(Question.choices)).where(Question.id == question_id))
        choice = db.get(AnswerChoice, choice_id)
        if not question or not choice or choice.question_id != question.id:
            raise HTTPException(status_code=400, detail="Invalid question or answer choice")
        is_correct = bool(choice.is_correct)
        correct_count += 1 if is_correct else 0
        db.add(QuizAnswer(attempt_id=attempt.id, question_id=question.id, selected_choice_id=choice.id, is_correct=is_correct))
        if not is_correct:
            mistake = db.scalar(select(MistakeBank).where(MistakeBank.user_id == user.id, MistakeBank.question_id == question.id))
            if mistake:
                mistake.times_missed += 1
                mistake.mastered_at = None
            else:
                db.add(MistakeBank(user_id=user.id, question_id=question.id, times_missed=1))
        results.append({"question": question_out(question, include_answer=True), "selected_choice_id": choice.id, "is_correct": is_correct})

    attempt.score = round(correct_count / max(len(payload.answers), 1) * 100)
    db.commit()
    return {"attempt_id": attempt.id, "score": attempt.score, "correct": correct_count, "total": len(payload.answers), "results": results}


@app.get("/api/progress")
def progress(request: Request, db: Session = Depends(get_db)):
    user = require_user(request, db)
    total_lessons = db.scalar(select(func.count()).select_from(Lesson).where(Lesson.is_active == True)) or 0
    progress_rows = db.scalars(select(LessonProgress).where(LessonProgress.user_id == user.id)).all()
    completed = sum(1 for p in progress_rows if p.completed)
    mistakes = db.scalar(select(func.count()).select_from(MistakeBank).where(MistakeBank.user_id == user.id)) or 0
    return {
        "total_lessons": total_lessons,
        "completed_lessons": completed,
        "percent_complete": round(completed / max(total_lessons, 1) * 100),
        "mistake_count": mistakes,
        "items": [
            {
                "lesson_id": p.lesson_id,
                "completed": p.completed,
                "confidence": p.confidence,
                "notes": p.notes,
                "saved_for_review": p.saved_for_review,
            }
            for p in progress_rows
        ],
    }


@app.post("/api/lessons/{lesson_id}/progress")
def save_lesson_progress(lesson_id: int, payload: LessonProgressIn, request: Request, db: Session = Depends(get_db)):
    user = require_user(request, db)
    lesson = db.get(Lesson, lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    row = db.scalar(select(LessonProgress).where(LessonProgress.user_id == user.id, LessonProgress.lesson_id == lesson.id))
    if not row:
        row = LessonProgress(user_id=user.id, lesson_id=lesson.id)
        db.add(row)
    row.completed = payload.completed
    row.confidence = payload.confidence
    row.notes = payload.notes
    row.saved_for_review = payload.saved_for_review
    db.commit()
    return {"ok": True}


@app.get("/api/mistakes")
def mistake_bank(request: Request, db: Session = Depends(get_db)):
    user = require_user(request, db)
    rows = db.scalars(select(MistakeBank).options(selectinload(MistakeBank.question).selectinload(Question.choices)).where(MistakeBank.user_id == user.id).order_by(MistakeBank.times_missed.desc())).all()
    return [
        {
            "id": m.id,
            "times_missed": m.times_missed,
            "question": question_out(m.question, include_answer=True),
        }
        for m in rows
    ]


@app.post("/api/tutor/ask")
def tutor_ask(payload: TutorAskIn, request: Request, db: Session = Depends(get_db)):
    user = require_user(request, db)
    rate_limit(f"tutor:{user.id}", 10, 60)
    return ask_coverage_coach(db, user, payload.message)


@app.get("/api/dashboard")
def dashboard(request: Request, db: Session = Depends(get_db)):
    """Aggregated progress data for the dashboard view."""
    user = require_user(request, db)

    # ── Lesson completion ────────────────────────────────────────────
    total_lessons = (
        db.scalar(select(func.count()).select_from(Lesson).where(Lesson.is_active == True)) or 0
    )
    progress_rows = db.scalars(
        select(LessonProgress).where(LessonProgress.user_id == user.id)
    ).all()
    completed_ids = {p.lesson_id for p in progress_rows if p.completed}

    # ── Module breakdown + recommendations ──────────────────────────
    modules = db.scalars(
        select(Module)
        .where(Module.is_active == True)
        .options(selectinload(Module.lessons))
        .order_by(Module.sort_order)
    ).all()

    module_stats: list[dict] = []
    recommendations: list[dict] = []
    for m in modules:
        active = [l for l in m.lessons if l.is_active]
        done = sum(1 for l in active if l.id in completed_ids)
        pct = round(done / max(len(active), 1) * 100)
        module_stats.append({
            "slug": m.slug,
            "title": m.title,
            "total_lessons": len(active),
            "completed_lessons": done,
            "pct": pct,
        })
        # First incomplete lesson per module → up-next recommendations
        if len(recommendations) < 4:
            for l in sorted(active, key=lambda x: x.sort_order):
                if l.id not in completed_ids:
                    recommendations.append({
                        "lesson_slug": l.slug,
                        "lesson_title": l.title,
                        "module_slug": m.slug,
                        "module_title": m.title,
                        "estimated_minutes": l.estimated_minutes or 7,
                    })
                    break

    # ── Quiz history ─────────────────────────────────────────────────
    recent_attempts = db.scalars(
        select(QuizAttempt)
        .where(QuizAttempt.user_id == user.id)
        .order_by(QuizAttempt.created_at.desc())
        .limit(10)
    ).all()
    avg_quiz = (
        round(sum(a.score for a in recent_attempts) / len(recent_attempts))
        if recent_attempts else 0
    )

    # ── Mistake bank ─────────────────────────────────────────────────
    mistake_count = (
        db.scalar(
            select(func.count()).select_from(MistakeBank).where(MistakeBank.user_id == user.id)
        ) or 0
    )
    top_mistakes = db.scalars(
        select(MistakeBank)
        .options(selectinload(MistakeBank.question))
        .where(MistakeBank.user_id == user.id)
        .order_by(MistakeBank.times_missed.desc())
        .limit(5)
    ).all()

    # ── Readiness score ──────────────────────────────────────────────
    lesson_pct = round(len(completed_ids) / max(total_lessons, 1) * 100)
    mistake_penalty = min(mistake_count * 2, 20)
    readiness = max(0, min(100, round(lesson_pct * 0.5 + avg_quiz * 0.5 - mistake_penalty)))

    return {
        "user": user.name or user.email or "Candidate",
        "readiness": readiness,
        "lessons": {
            "total": total_lessons,
            "completed": len(completed_ids),
            "pct": lesson_pct,
        },
        "quizzes": {
            "total_taken": len(recent_attempts),
            "avg_score": avg_quiz,
            "recent": [
                {
                    "score": a.score,
                    "total": a.total_questions,
                    "date": a.created_at.isoformat() if a.created_at else None,
                }
                for a in recent_attempts[:8]
            ],
        },
        "mistakes": {
            "count": mistake_count,
            "top": [
                {
                    "question": (
                        m.question.question_text[:110] + "…"
                        if m.question and len(m.question.question_text) > 110
                        else (m.question.question_text if m.question else "")
                    ),
                    "times_missed": m.times_missed,
                }
                for m in top_mistakes
            ],
        },
        "modules": module_stats,
        "recommendations": recommendations,
    }


@app.get("/api/study-plan/summary")
def study_plan_summary(request: Request, db: Session = Depends(get_db)) -> dict[str, Any]:
    """Lightweight plan summary — no Ollama, returns top-2 plan steps in <100ms."""
    user = require_user(request, db)
    data = _compute_study_plan(user, db)
    return {"summary": data["summary"], "plan": data["plan"][:2]}


@app.get("/api/study-plan")
def study_plan(request: Request, db: Session = Depends(get_db)) -> dict[str, Any]:
    user = require_user(request, db)
    data = _compute_study_plan(user, db)
    summary = data["summary"]
    plan = data["plan"]
    weak_areas = data["weak_areas"]
    strengths = data["strengths"]
    tested = data["tested"]
    review_due = summary["review_items_due"]

    # ── Ollama narrative ─────────────────────────────────────────────
    narrative_prompt = (
        f"Student summary: {summary['modules_mastered']} of {summary['modules_total']} modules mastered, "
        f"overall quiz average {summary['overall_readiness']}%, "
        f"{review_due} mistake-bank items due for review. "
        + (f"Weak areas: {', '.join(s['title'] for s in weak_areas[:3])}. " if weak_areas else "No weak areas yet. ")
        + (f"Strengths: {', '.join(s['title'] for s in strengths[:3])}. " if strengths else "")
        + "Write a 100-120 word personalised, encouraging study plan narrative in second person. "
        "Be specific about what they should focus on next. No bullet points, just flowing prose."
    )
    raw_narrative = call_ollama_raw(
        "You are Coverage Coach, a supportive P&C insurance licensing study tutor.",
        narrative_prompt,
    )
    if not raw_narrative:
        if not tested:
            raw_narrative = (
                "Welcome to your personalized study plan! Since you're just getting started, "
                "your first priority is to work through the foundation modules. Open each module, "
                "read through the lessons at your own pace, and take the practice quiz when you "
                "feel ready. The study plan will adapt as you build your progress — your next check-in "
                "will show your weak spots, spaced-repetition reviews, and confidence gaps. "
                "You've got this — every expert started exactly where you are now."
            )
        else:
            weak_titles = ", ".join(s["title"] for s in weak_areas[:2]) if weak_areas else "all areas"
            raw_narrative = (
                f"Great progress so far! Focus your energy on {weak_titles} where your quiz scores "
                "show room for improvement. Work through the lessons again, pay close attention to the "
                "glossary terms, and re-quiz until you hit 80%. Don't forget to clear your spaced-repetition "
                f"review queue — you have {review_due} items waiting. Once those are solid, revisit the "
                "modules where your confidence is high but accuracy is low to make sure your instincts "
                "match the exam material. Keep the momentum going!"
            )

    return {
        "summary": summary,
        "narrative": raw_narrative,
        "plan": plan[:8],
        "weak_areas": [{"slug": s["slug"], "title": s["title"], "accuracy": s["accuracy"]} for s in weak_areas[:5]],
        "strengths": [{"slug": s["slug"], "title": s["title"], "accuracy": s["accuracy"]} for s in strengths[:5]],
    }


def _compute_study_plan(user: Any, db: Session) -> dict[str, Any]:
    """Shared computation for both summary and full study-plan endpoints."""
    all_modules = db.scalars(select(Module).where(Module.is_active == True).order_by(Module.sort_order)).all()  # noqa: E712

    module_accuracy: dict[int, dict[str, Any]] = {}
    for mod in all_modules:
        total_ans = db.scalar(
            select(func.count()).select_from(QuizAnswer)
            .join(Question, QuizAnswer.question_id == Question.id)
            .join(QuizAttempt, QuizAnswer.attempt_id == QuizAttempt.id)
            .where(QuizAttempt.user_id == user.id, Question.module_id == mod.id)
        ) or 0
        correct_ans = db.scalar(
            select(func.count()).select_from(QuizAnswer)
            .join(Question, QuizAnswer.question_id == Question.id)
            .join(QuizAttempt, QuizAnswer.attempt_id == QuizAttempt.id)
            .where(QuizAttempt.user_id == user.id, Question.module_id == mod.id, QuizAnswer.is_correct == True)  # noqa: E712
        ) or 0
        accuracy = round(correct_ans / total_ans * 100) if total_ans else None

        lessons = db.scalars(
            select(Lesson).where(Lesson.module_id == mod.id, Lesson.is_active == True)  # noqa: E712
        ).all()
        lesson_ids = [l.id for l in lessons]
        progress_rows = db.scalars(
            select(LessonProgress).where(
                LessonProgress.user_id == user.id,
                LessonProgress.lesson_id.in_(lesson_ids),
            )
        ).all() if lesson_ids else []
        completed = [p for p in progress_rows if p.completed]
        confidences = [p.confidence for p in progress_rows if p.confidence]
        avg_conf = round(sum(confidences) / len(confidences), 1) if confidences else None
        lesson_pct = round(len(completed) / len(lesson_ids) * 100) if lesson_ids else 0

        module_accuracy[mod.id] = {
            "id": mod.id,
            "slug": mod.slug,
            "title": mod.title,
            "accuracy": accuracy,
            "total_answers": total_ans,
            "lesson_pct": lesson_pct,
            "avg_confidence": avg_conf,
            "total_lessons": len(lesson_ids),
            "completed_lessons": len(completed),
        }

    # Incorporate diagnostic results for untested modules
    diag = db.scalar(select(DiagnosticResult).where(DiagnosticResult.user_id == user.id))
    diag_scores: dict[str, int] = json.loads(diag.module_scores or "{}") if diag else {}
    for mod in all_modules:
        stat = module_accuracy[mod.id]
        if stat["accuracy"] is None and mod.slug in diag_scores:
            # Synthetic accuracy: 100% if correct in diagnostic, 30% if wrong (weak signal)
            stat["accuracy"] = 100 if diag_scores[mod.slug] == 1 else 30
            stat["_from_diagnostic"] = True

    due_mistakes = db.scalars(
        select(MistakeBank)
        .options(selectinload(MistakeBank.question))
        .where(MistakeBank.user_id == user.id, MistakeBank.mastered_at == None)  # noqa: E711
        .order_by(MistakeBank.last_missed_at.asc())
        .limit(8)
    ).all()

    stats = list(module_accuracy.values())
    tested = [s for s in stats if s["accuracy"] is not None]
    untested = [s for s in stats if s["accuracy"] is None and s["lesson_pct"] < 100]

    weak_areas: list[dict[str, Any]] = []
    strengths: list[dict[str, Any]] = []
    for s in tested:
        if s["accuracy"] < 65:
            weak_areas.append(s)
        elif s["accuracy"] >= 80 and s["lesson_pct"] == 100:
            strengths.append(s)

    conf_gap = [
        s for s in tested
        if s["avg_confidence"] is not None and s["avg_confidence"] >= 2.5 and s["accuracy"] < 70
    ]

    plan: list[dict[str, Any]] = []

    reviewed_module_ids: set[int] = set()
    for mb in due_mistakes[:3]:
        if mb.question and mb.question.module_id not in reviewed_module_ids:
            mod_stat = module_accuracy.get(mb.question.module_id)
            if mod_stat:
                plan.append({
                    "type": "spaced_review",
                    "module_slug": mod_stat["slug"],
                    "module_title": mod_stat["title"],
                    "reason": f"You've missed questions here {mb.times_missed}x — spaced repetition review is due.",
                    "action_label": "Review Mistakes",
                })
                reviewed_module_ids.add(mb.question.module_id)

    for s in sorted(weak_areas, key=lambda x: x["accuracy"])[:3]:
        if not any(p["module_slug"] == s["slug"] for p in plan):
            plan.append({
                "type": "weak_module",
                "module_slug": s["slug"],
                "module_title": s["title"],
                "reason": f"Quiz accuracy is {s['accuracy']}% — needs focused practice.",
                "action_label": "Study & Quiz",
            })

    for s in conf_gap[:2]:
        if not any(p["module_slug"] == s["slug"] for p in plan):
            plan.append({
                "type": "confidence_gap",
                "module_slug": s["slug"],
                "module_title": s["title"],
                "reason": f"You feel confident ({s['avg_confidence']}/3) but quiz accuracy is only {s['accuracy']}% — review to solidify.",
                "action_label": "Solidify Knowledge",
            })

    for s in sorted(untested, key=lambda x: x["total_lessons"])[:3]:
        if not any(p["module_slug"] == s["slug"] for p in plan):
            plan.append({
                "type": "start_here",
                "module_slug": s["slug"],
                "module_title": s["title"],
                "reason": "You haven't studied this module yet — start here to build your foundation.",
                "action_label": "Start Module",
            })

    for s in stats:
        if 80 <= s["lesson_pct"] < 100 and not any(p["module_slug"] == s["slug"] for p in plan):
            plan.append({
                "type": "finish_module",
                "module_slug": s["slug"],
                "module_title": s["title"],
                "reason": f"You've completed {s['lesson_pct']}% of lessons — finish the module to lock in mastery.",
                "action_label": "Finish Module",
            })

    mastered = [s for s in stats if s["lesson_pct"] == 100 and (s["accuracy"] or 0) >= 75]
    review_due = len(due_mistakes)
    overall_readiness = round(
        db.scalar(select(func.avg(QuizAttempt.score)).where(QuizAttempt.user_id == user.id)) or 0
    )

    return {
        "summary": {
            "overall_readiness": overall_readiness,
            "modules_mastered": len(mastered),
            "modules_total": len(all_modules),
            "review_items_due": review_due,
        },
        "plan": plan[:8],
        "weak_areas": weak_areas,
        "strengths": strengths,
        "tested": tested,
    }


# ── Diagnostic placement quiz ─────────────────────────────────────────────────

DIAGNOSTIC_MODULES = [
    "insurance-basics",
    "property-fundamentals",
    "casualty-fundamentals",
    "personal-auto",
    "homeowners",
]


def _format_question_with_module(q: Question) -> dict[str, Any]:
    return {
        "id": q.id,
        "question_text": q.question_text,
        "question_type": q.question_type,
        "difficulty": q.difficulty,
        "module_slug": q.module.slug if q.module else "",
        "module_title": q.module.title if q.module else "",
        "choices": [
            {"id": c.id, "choice_text": c.choice_text, "sort_order": c.sort_order}
            for c in sorted(q.choices, key=lambda c: c.sort_order)
        ],
    }


@app.get("/api/diagnostic/questions")
def diagnostic_questions(db: Session = Depends(get_db)) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for slug in DIAGNOSTIC_MODULES:
        mod = db.scalar(select(Module).where(Module.slug == slug, Module.is_active == True))  # noqa: E712
        if not mod:
            continue
        questions = db.scalars(
            select(Question)
            .options(selectinload(Question.choices), selectinload(Question.module))
            .where(Question.module_id == mod.id, Question.is_active == True)  # noqa: E712
        ).all()
        if questions:
            result.append(_format_question_with_module(random.choice(questions)))
    return result


@app.post("/api/diagnostic/submit")
def diagnostic_submit(
    body: DiagnosticSubmitIn,
    request: Request,
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    user = require_user(request, db)

    # One diagnostic per user — idempotent upsert
    existing = db.scalar(select(DiagnosticResult).where(DiagnosticResult.user_id == user.id))

    module_scores: dict[str, int] = {}
    score = 0
    for q_id, choice_id in body.answers.items():
        q = db.scalar(
            select(Question)
            .options(selectinload(Question.choices), selectinload(Question.module))
            .where(Question.id == int(q_id))
        )
        if not q:
            continue
        correct_choice = next((c for c in q.choices if c.is_correct), None)
        is_correct = correct_choice is not None and correct_choice.id == int(choice_id)
        if q.module:
            module_scores[q.module.slug] = 1 if is_correct else 0
        if is_correct:
            score += 1

    if existing:
        existing.score = score
        existing.module_scores = json.dumps(module_scores)
        from datetime import datetime, timezone
        existing.completed_at = datetime.now(timezone.utc)
    else:
        db.add(DiagnosticResult(
            user_id=user.id,
            score=score,
            module_scores=json.dumps(module_scores),
        ))
    db.commit()

    return {
        "score": score,
        "total": len(DIAGNOSTIC_MODULES),
        "module_scores": module_scores,
        "already_had_diagnostic": existing is not None,
    }


@app.get("/api/diagnostic/status")
def diagnostic_status(request: Request, db: Session = Depends(get_db)) -> dict[str, Any]:
    user = require_user(request, db)
    result = db.scalar(select(DiagnosticResult).where(DiagnosticResult.user_id == user.id))
    if not result:
        return {"completed": False, "score": None, "module_scores": None}
    return {
        "completed": True,
        "score": result.score,
        "module_scores": json.loads(result.module_scores or "{}"),
    }


# ── Flashcards ────────────────────────────────────────────────────────────────

def _sm2(ease: float, interval: float, rating: int) -> tuple[float, float]:
    if rating == 1:
        return 1.3, 1.0
    elif rating == 2:
        return max(1.3, ease - 0.15), max(1.0, interval * 1.2)
    elif rating == 3:
        return ease, interval * ease
    else:
        return min(4.0, ease + 0.15), interval * min(4.0, ease + 0.15) * 1.3


def _term_to_card(term: Term, progress: FlashcardProgress | None, now: datetime) -> dict[str, Any]:
    due = progress is None or progress.next_review <= now
    return {
        "id": term.id,
        "term": term.term,
        "definition": term.exam_definition or term.plain_english_definition or "",
        "example": term.example or "",
        "module_title": term.module.title if term.module else "",
        "module_slug": term.module.slug if term.module else "",
        "due": due,
        "interval_days": round(progress.interval_days, 2) if progress else 1.0,
        "ease": round(progress.ease, 2) if progress else 2.5,
        "review_count": progress.review_count if progress else 0,
    }


@app.get("/api/flashcards")
def get_flashcards(
    module_slug: str | None = None,
    request: Request = None,
    db: Session = Depends(get_db),
) -> list[dict[str, Any]]:
    user = require_user(request, db)
    now = datetime.now(timezone.utc)

    q = select(Term).options(selectinload(Term.module))
    if module_slug:
        mod = db.scalar(select(Module).where(Module.slug == module_slug))
        if mod:
            q = q.where(Term.module_id == mod.id)
    terms = db.scalars(q).all()

    progress_map: dict[int, FlashcardProgress] = {
        p.term_id: p
        for p in db.scalars(
            select(FlashcardProgress).where(FlashcardProgress.user_id == user.id)
        ).all()
    }

    cards = [_term_to_card(t, progress_map.get(t.id), now) for t in terms]
    # Due cards first, then new/not-due — both groups shuffled
    due = [c for c in cards if c["due"]]
    not_due = [c for c in cards if not c["due"]]
    random.shuffle(due)
    random.shuffle(not_due)
    return due + not_due


@app.post("/api/flashcards/{term_id}/review")
def review_flashcard(
    term_id: int,
    payload: FlashcardReviewIn,
    request: Request,
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    user = require_user(request, db)
    now = datetime.now(timezone.utc)

    term = db.scalar(select(Term).where(Term.id == term_id))
    if not term:
        raise HTTPException(status_code=404, detail="Term not found")

    progress = db.scalar(
        select(FlashcardProgress).where(
            FlashcardProgress.user_id == user.id,
            FlashcardProgress.term_id == term_id,
        )
    )
    if not progress:
        progress = FlashcardProgress(user_id=user.id, term_id=term_id)
        db.add(progress)

    new_ease, new_interval = _sm2(progress.ease, progress.interval_days, payload.rating)
    progress.ease = new_ease
    progress.interval_days = new_interval
    progress.review_count = (progress.review_count or 0) + 1
    progress.last_reviewed = now
    progress.next_review = now + timedelta(days=new_interval)
    db.commit()
    db.refresh(progress)

    return {
        "term_id": term_id,
        "ease": round(progress.ease, 2),
        "interval_days": round(progress.interval_days, 2),
        "review_count": progress.review_count,
        "next_review": progress.next_review.isoformat(),
    }


# ── Exam Session ──────────────────────────────────────────────────────────────

@app.get("/api/exam/start")
def exam_start(request: Request, db: Session = Depends(get_db)) -> dict[str, Any]:
    user = require_user(request, db)

    all_modules = db.scalars(select(Module).where(Module.is_active == True)).all()
    questions_per_module: dict[int, list[Question]] = {}
    for mod in all_modules:
        qs = db.scalars(
            select(Question)
            .options(selectinload(Question.choices), selectinload(Question.module))
            .where(Question.module_id == mod.id)
        ).all()
        if qs:
            questions_per_module[mod.id] = list(qs)

    # Proportional allocation up to 50 questions
    total_available = sum(len(v) for v in questions_per_module.values())
    target = min(50, total_available)
    selected: list[Question] = []
    if questions_per_module:
        base = max(1, target // len(questions_per_module))
        for mod_id, qs in questions_per_module.items():
            pick = random.sample(qs, min(base, len(qs)))
            selected.extend(pick)
        # Top up to target if under
        used_ids = {q.id for q in selected}
        remaining = [q for qs in questions_per_module.values() for q in qs if q.id not in used_ids]
        random.shuffle(remaining)
        selected.extend(remaining[: max(0, target - len(selected))])

    random.shuffle(selected)

    exam_id = str(uuid.uuid4())
    session = ExamSession(
        id=exam_id,
        user_id=user.id,
        total_questions=len(selected),
    )
    db.add(session)
    db.commit()

    def _q_out(q: Question) -> dict[str, Any]:
        choices = list(q.choices)
        random.shuffle(choices)
        return {
            "id": q.id,
            "question_text": q.question_text,
            "module_title": q.module.title if q.module else "",
            "module_slug": q.module.slug if q.module else "",
            "choices": [{"id": c.id, "text": c.choice_text} for c in choices],
        }

    return {
        "exam_id": exam_id,
        "questions": [_q_out(q) for q in selected],
        "total": len(selected),
        "time_limit_minutes": 90,
    }


@app.post("/api/exam/{exam_id}/submit")
def exam_submit(
    exam_id: str,
    payload: ExamSubmitIn,
    request: Request,
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    user = require_user(request, db)
    session = db.scalar(select(ExamSession).where(ExamSession.id == exam_id, ExamSession.user_id == user.id))
    if not session:
        raise HTTPException(status_code=404, detail="Exam not found")
    if session.status == "completed":
        return json.loads(session.results_json)

    now = datetime.now(timezone.utc)
    started = session.started_at
    if started.tzinfo is None:
        started = started.replace(tzinfo=timezone.utc)
    time_taken = round((now - started).total_seconds() / 60, 1)

    correct_total = 0
    module_scores: dict[str, dict[str, Any]] = {}
    missed_questions: list[dict[str, Any]] = []

    for q_id_str, choice_id in payload.answers.items():
        q = db.scalar(
            select(Question)
            .options(selectinload(Question.choices), selectinload(Question.module))
            .where(Question.id == int(q_id_str))
        )
        if not q:
            continue
        correct_choice = next((c for c in q.choices if c.is_correct), None)
        chosen_choice = next((c for c in q.choices if c.id == int(choice_id)), None)
        is_correct = correct_choice is not None and chosen_choice is not None and correct_choice.id == chosen_choice.id

        slug = q.module.slug if q.module else "unknown"
        title = q.module.title if q.module else "Unknown"
        if slug not in module_scores:
            module_scores[slug] = {"title": title, "correct": 0, "total": 0, "pct": 0}
        module_scores[slug]["total"] += 1
        if is_correct:
            correct_total += 1
            module_scores[slug]["correct"] += 1
        else:
            missed_questions.append({
                "id": q.id,
                "question_text": q.question_text,
                "correct_answer": correct_choice.choice_text if correct_choice else "",
                "your_answer": chosen_choice.choice_text if chosen_choice else "No answer",
                "module_title": title,
            })
            # Add to mistake bank
            existing_mistake = db.scalar(
                select(MistakeBank).where(MistakeBank.user_id == user.id, MistakeBank.question_id == q.id)
            )
            if existing_mistake:
                existing_mistake.times_missed += 1
                existing_mistake.last_missed_at = now
            else:
                db.add(MistakeBank(user_id=user.id, question_id=q.id, times_missed=1))

    for slug in module_scores:
        s = module_scores[slug]
        s["pct"] = round(s["correct"] / s["total"] * 100) if s["total"] else 0

    total_q = max(1, len(payload.answers))
    score_pct = round(correct_total / total_q * 100)
    passed = score_pct >= 70

    results = {
        "score": score_pct,
        "passed": passed,
        "correct": correct_total,
        "total": total_q,
        "time_taken_minutes": time_taken,
        "module_scores": module_scores,
        "missed_questions": missed_questions[:20],
    }

    session.status = "completed"
    session.completed_at = now
    session.score = score_pct
    session.answers_json = json.dumps({str(k): v for k, v in payload.answers.items()})
    session.results_json = json.dumps(results)
    db.commit()

    return results


@app.get("/api/exam/{exam_id}/results")
def exam_results(exam_id: str, request: Request, db: Session = Depends(get_db)) -> dict[str, Any]:
    user = require_user(request, db)
    session = db.scalar(select(ExamSession).where(ExamSession.id == exam_id, ExamSession.user_id == user.id))
    if not session or session.status != "completed":
        raise HTTPException(status_code=404, detail="Results not available")
    return json.loads(session.results_json)


# ── Account deletion ──────────────────────────────────────────────────────────

@app.delete("/api/account")
def delete_account(request: Request, db: Session = Depends(get_db)) -> dict[str, Any]:
    user = require_user(request, db)
    db.delete(user)
    db.commit()
    request.session.clear()
    return {"ok": True, "message": "Account and all data deleted."}


# ── Privacy & Terms ───────────────────────────────────────────────────────────

_PRIVACY_HTML = """<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Privacy Policy — P&C Prep Academy</title>
<style>body{font-family:system-ui,sans-serif;max-width:720px;margin:40px auto;padding:0 20px;line-height:1.7;color:#222}
h1{font-size:1.6rem}h2{font-size:1.1rem;margin-top:2em}a{color:#6366f1}code{background:#f3f4f6;padding:2px 6px;border-radius:4px}</style>
</head><body>
<h1>Privacy Policy</h1>
<p><em>Last updated: June 2026</em></p>
<h2>What data we collect</h2>
<p>When you sign in with Google, Microsoft, or Facebook we receive your <strong>email address</strong> and <strong>display name</strong>. No password is stored.</p>
<p>As you study, we store: lesson completion records, quiz scores, practice quiz answers, mistake bank entries, flashcard review history, diagnostic quiz results, and exam simulation sessions. All of this is stored only to power your personalised study plan.</p>
<h2>How data is used</h2>
<p>Your data is used solely to provide the P&amp;C Prep Academy service. It is <strong>never sold</strong> and <strong>never shared with third parties</strong>.</p>
<h2>Where data is stored</h2>
<p>All data is stored on our own server. We do not use third-party analytics or advertising services.</p>
<h2>How to delete your data</h2>
<p>You can permanently delete your account and all associated data by sending a <code>DELETE /api/account</code> request while signed in. This is irreversible and cascades to all study records.</p>
<h2>Cookies</h2>
<p>We use a single session cookie to keep you signed in. No tracking or advertising cookies are used.</p>
<h2>Contact</h2>
<p>Questions? Email <a href="mailto:logan@weinsurethings.com">logan@weinsurethings.com</a>.</p>
<p><a href="/">← Back to app</a></p>
</body></html>"""

_TERMS_HTML = """<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Terms of Use — P&C Prep Academy</title>
<style>body{font-family:system-ui,sans-serif;max-width:720px;margin:40px auto;padding:0 20px;line-height:1.7;color:#222}
h1{font-size:1.6rem}h2{font-size:1.1rem;margin-top:2em}a{color:#6366f1}</style>
</head><body>
<h1>Terms of Use</h1>
<p><em>Last updated: June 2026</em></p>
<h2>Educational tool only</h2>
<p>P&amp;C Prep Academy is a free educational study tool. It is designed to help you prepare for the P&amp;C insurance licensing exam. It does <strong>not</strong> guarantee that you will pass the exam.</p>
<h2>Not professional or legal advice</h2>
<p>Nothing on this platform constitutes professional, legal, or insurance advice. Study content is prepared for educational purposes only.</p>
<h2>Age requirement</h2>
<p>You must be 18 years of age or older to use this service, or have obtained parental/guardian consent.</p>
<h2>No warranty</h2>
<p>This service is provided "as is" without warranty of any kind. We make no representations about the accuracy or completeness of the study content.</p>
<h2>Account termination</h2>
<p>We reserve the right to suspend or delete accounts that misuse the platform.</p>
<h2>Changes to terms</h2>
<p>We may update these terms at any time. Continued use of the service constitutes acceptance of the current terms.</p>
<p><a href="/">← Back to app</a></p>
</body></html>"""


@app.get("/privacy", response_class=HTMLResponse)
def privacy() -> str:
    return _PRIVACY_HTML


@app.get("/terms", response_class=HTMLResponse)
def terms_page() -> str:
    return _TERMS_HTML
