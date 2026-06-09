from __future__ import annotations

import random
from contextlib import asynccontextmanager
from typing import Any

from fastapi import Depends, FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload
from starlette.middleware.sessions import SessionMiddleware

from .auth import configured_providers, dev_login, login_redirect, oauth_callback, public_user, require_user
from .content_loader import seed_course_if_empty
from .database import SessionLocal, create_all, get_db
from .models import AnswerChoice, Lesson, LessonProgress, MistakeBank, Module, Question, QuizAnswer, QuizAttempt, Term, User
from .settings import settings
from .tutor import ask_coverage_coach

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


class CourseIn(BaseModel):
    course: str = Field(pattern="^(pc|lh)$")


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_all()
    db = SessionLocal()
    try:
        seed_course_if_empty(db)
        # Backfill course column on any modules that predate this field
        db.execute(__import__("sqlalchemy").text("UPDATE modules SET course='pc' WHERE course IS NULL OR course=''"))
        db.commit()
    finally:
        db.close()
    yield


app = FastAPI(title="P&C License Prep Academy API", version="2.1.0", lifespan=lifespan)
origins = settings.cors_origin_list
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False if origins == ["*"] else True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SessionMiddleware, secret_key=settings.session_secret, same_site="lax", https_only=settings.app_base_url.startswith("https"))

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
        "coverage_coach_mode": "openai" if settings.openai_api_key else "fallback",
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
    user = db.get(User, int(user_id))
    return {"user": public_user(user) if user else None}


@app.post("/api/me/course")
def set_course(payload: CourseIn, request: Request, db: Session = Depends(get_db)):
    user = require_user(request, db)
    user.course = payload.course
    db.commit()
    return {"ok": True, "course": user.course}


@app.get("/api/modules")
def list_modules(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    course = "pc"
    if user_id:
        user = db.get(User, int(user_id))
        if user:
            course = user.course or "pc"
    modules = db.scalars(
        select(Module)
        .options(selectinload(Module.lessons))
        .where(Module.is_active == True, Module.course == course)
        .order_by(Module.sort_order, Module.id)
    ).all()
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
    return ask_coverage_coach(db, user, payload.message)


@app.get("/api/dashboard")
def dashboard(request: Request, db: Session = Depends(get_db)):
    """Aggregated progress data for the dashboard view."""
    user = require_user(request, db)

    course = user.course or "pc"

    # ── Lesson completion ────────────────────────────────────────────
    total_lessons = (
        db.scalar(
            select(func.count()).select_from(Lesson)
            .join(Module, Module.id == Lesson.module_id)
            .where(Lesson.is_active == True, Module.course == course)
        ) or 0
    )
    progress_rows = db.scalars(
        select(LessonProgress).where(LessonProgress.user_id == user.id)
    ).all()
    completed_ids = {p.lesson_id for p in progress_rows if p.completed}

    # ── Module breakdown + recommendations ──────────────────────────
    modules = db.scalars(
        select(Module)
        .where(Module.is_active == True, Module.course == course)
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
