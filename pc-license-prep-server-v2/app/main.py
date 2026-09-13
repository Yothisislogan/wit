from __future__ import annotations

import random
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Any, Literal

from fastapi import Depends, FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from sqlalchemy import case, func, inspect, select, text
from sqlalchemy.orm import Session, selectinload
from starlette.middleware.sessions import SessionMiddleware

from .auth import configured_providers, login_redirect, oauth_callback, public_user, require_user
from .content_loader import seed_course_if_empty
from .database import SessionLocal, create_all, get_db
from .models import AnswerChoice, Lesson, LessonProgress, MistakeBank, Module, Question, QuizAnswer, QuizAttempt, Term, User
from .settings import settings
from .study_scope import module_scope
from .exam_profiles import STATE_EXAM_INFO, state_profile
from .exams import router as exams_router
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


class StateIn(BaseModel):
    state: str = Field(min_length=2, max_length=2, pattern="^[A-Z]{2}$")


_STATE_NAMES: dict[str, str] = {k: v["state_name"] for k, v in STATE_EXAM_INFO.items()}


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_all()
    db = SessionLocal()
    try:
        # Inspect legacy columns; unexpected migration errors must fail startup.
        for table, additions in {
            "users": {"course": "VARCHAR(20) DEFAULT 'pc'", "state": "VARCHAR(2)", "anon_id": "VARCHAR(64)"},
            "modules": {"course": "VARCHAR(20) DEFAULT 'pc'"},
        }.items():
            columns = {column["name"] for column in inspect(db.bind).get_columns(table)}
            for name, definition in additions.items():
                if name not in columns:
                    db.execute(text(f"ALTER TABLE {table} ADD COLUMN {name} {definition}"))
        db.execute(text("CREATE INDEX IF NOT EXISTS idx_users_anon_id ON users(anon_id)"))
        db.commit()
        seed_course_if_empty(db)
    finally:
        db.close()
    yield


app = FastAPI(title="P&C License Prep Academy API", version="2.1.0", lifespan=lifespan)
app.include_router(exams_router)
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
        "lesson_count": sum(1 for lesson in module.lessons if lesson.is_active),
        "content_review_status": "pending",
        "is_state_law": module.slug.startswith("state-law-"),
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
    choices = list(question.choices)
    if not include_answer:
        random.shuffle(choices)
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
                "sort_order": position,
                **({"is_correct": c.is_correct} if include_answer else {}),
            }
            for position, c in enumerate(choices)
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
        "coverage_coach_mode": settings.coverage_coach_provider if settings.gemini_api_key else ("openai" if settings.openai_api_key else "fallback"),
    }


@app.get("/auth/providers")
def auth_providers():
    return {"providers": configured_providers()}


@app.get("/auth/login/{provider}")
async def login(provider: str, request: Request):
    return await login_redirect(request, provider)


@app.get("/auth/callback/{provider}")
async def callback(provider: str, request: Request, db: Session = Depends(get_db)):
    return await oauth_callback(request, db, provider)


@app.post("/auth/logout")
def logout(request: Request):
    request.session.clear()
    return {"ok": True}


@app.get("/api/me")
def me(request: Request, db: Session = Depends(get_db)):
    user = require_user(request, db)
    base = public_user(user)
    course = getattr(user, "course", "pc") or "pc"
    state = getattr(user, "state", None)
    state_name = STATE_EXAM_INFO.get(state or "", {}).get("state_name") if state else None
    return {"user": {**base, "course": course, "state": state, "state_name": state_name, "is_anon": user.email is None}}


@app.post("/api/me/course")
def set_course(payload: CourseIn, request: Request, db: Session = Depends(get_db)):
    user = require_user(request, db)
    user.course = payload.course
    db.commit()
    return {"ok": True, "course": user.course}


@app.post("/api/me/state")
def set_state(payload: StateIn, request: Request, db: Session = Depends(get_db)):
    if payload.state not in STATE_EXAM_INFO:
        raise HTTPException(status_code=422, detail=f"Unknown state abbreviation: {payload.state}")
    user = require_user(request, db)
    user.state = payload.state
    db.commit()
    return {"ok": True, "state": user.state, "state_name": _STATE_NAMES[user.state]}


@app.get("/api/state-info/{state_abbr}")
def state_info(state_abbr: str):
    abbr = state_abbr.upper()
    if abbr not in STATE_EXAM_INFO:
        raise HTTPException(status_code=404, detail="State not found")
    return state_profile(abbr)


@app.get("/api/modules")
def list_modules(request: Request, course: Literal["pc", "lh"] | None = Query(None), db: Session = Depends(get_db)):
    user = require_user(request, db)
    stmt = select(Module).options(selectinload(Module.lessons)).where(module_scope(user, course))
    stmt = stmt.order_by(Module.sort_order, Module.id)
    modules = db.scalars(stmt).all()
    return [module_out(m) for m in modules]


@app.get("/api/modules/{slug}")
def get_module(slug: str, request: Request, db: Session = Depends(get_db)):
    user = require_user(request, db)
    module = db.scalar(select(Module).options(selectinload(Module.lessons)).where(Module.slug == slug, module_scope(user)))
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    return {**module_out(module), "lessons": [lesson_out(l) for l in module.lessons if l.is_active]}


@app.get("/api/lessons/{slug}")
def get_lesson(slug: str, request: Request, db: Session = Depends(get_db)):
    user = require_user(request, db)
    lesson = db.scalar(select(Lesson).join(Module).where(Lesson.slug == slug, Lesson.is_active == True, module_scope(user)))
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    terms = db.scalars(select(Term).where(Term.module_id == lesson.module_id).order_by(Term.term)).all()
    module = db.scalar(select(Module).where(Module.id == lesson.module_id))
    saved = db.scalar(select(LessonProgress).where(LessonProgress.user_id == user.id, LessonProgress.lesson_id == lesson.id))
    return {
        **lesson_out(lesson),
        "module_slug": module.slug if module else "",
        "module_title": module.title if module else "",
        "terms": [term_out(t) for t in terms],
        "progress": lesson_progress_out(saved, lesson.id),
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
def list_terms(request: Request, module_slug: str | None = None, db: Session = Depends(get_db)):
    user = require_user(request, db)
    stmt = select(Term).join(Module).where(module_scope(user)).order_by(Term.term)
    if module_slug:
        stmt = stmt.where(Module.slug == module_slug)
    return [term_out(t) for t in db.scalars(stmt).all()]


@app.get("/api/questions")
def list_questions(request: Request, module_slug: str | None = None, limit: int = Query(10, ge=1, le=50), mistakes_only: bool = False, db: Session = Depends(get_db)):
    user = require_user(request, db)
    stmt = select(Question).join(Module).options(selectinload(Question.choices)).where(Question.is_active == True, module_scope(user))
    if module_slug:
        stmt = stmt.where(Module.slug == module_slug)
    if mistakes_only:
        stmt = stmt.join(MistakeBank).where(MistakeBank.user_id == user.id, MistakeBank.mastered_at.is_(None))
    questions = list(db.scalars(stmt).all())
    # An incomplete content import should never serve an unanswerable question.
    questions = [q for q in questions if len(q.choices) >= 2 and sum(bool(c.is_correct) for c in q.choices) == 1]
    random.shuffle(questions)
    return [question_out(q) for q in questions[:limit]]


@app.post("/api/quiz/submit")
def submit_quiz(payload: QuizSubmitIn, request: Request, db: Session = Depends(get_db)):
    user = require_user(request, db)
    if not 1 <= len(payload.answers) <= 50:
        raise HTTPException(status_code=400, detail="Submit between 1 and 50 answers at a time")

    attempt = QuizAttempt(user_id=user.id, mode=payload.mode, total_questions=len(payload.answers))
    db.add(attempt)
    db.flush()

    correct_count = 0
    results = []
    for question_id, choice_id in payload.answers.items():
        question = db.scalar(select(Question).join(Module).options(selectinload(Question.choices)).where(Question.id == question_id, Question.is_active == True, module_scope(user)))
        choice = db.get(AnswerChoice, choice_id)
        if not question or not choice or choice.question_id != question.id:
            raise HTTPException(status_code=400, detail="Invalid question or answer choice")
        if len(question.choices) < 2 or sum(bool(c.is_correct) for c in question.choices) != 1:
            raise HTTPException(status_code=400, detail="This question is unavailable. Please start a new quiz.")
        is_correct = bool(choice.is_correct)
        correct_count += 1 if is_correct else 0
        db.add(QuizAnswer(attempt_id=attempt.id, question_id=question.id, selected_choice_id=choice.id, is_correct=is_correct))
        mistake = db.scalar(select(MistakeBank).where(MistakeBank.user_id == user.id, MistakeBank.question_id == question.id))
        if not is_correct:
            if mistake:
                mistake.times_missed += 1
                mistake.mastered_at = None
                mistake.last_missed_at = datetime.now(timezone.utc)
            else:
                db.add(MistakeBank(user_id=user.id, question_id=question.id, times_missed=1))
        elif mistake:
            # Keep history, but remove a corrected answer from the active queue.
            mistake.mastered_at = datetime.now(timezone.utc)
        results.append({"question": question_out(question, include_answer=True), "selected_choice_id": choice.id, "is_correct": is_correct})

    attempt.score = round(correct_count / max(len(payload.answers), 1) * 100)
    db.commit()
    return {"attempt_id": attempt.id, "score": attempt.score, "correct": correct_count, "total": len(payload.answers), "results": results}


def lesson_progress_out(row: LessonProgress | None, lesson_id: int) -> dict[str, Any]:
    return {
        "lesson_id": lesson_id,
        "completed": row.completed if row else False,
        "confidence": row.confidence if row else 0,
        "notes": row.notes if row else "",
        "saved_for_review": row.saved_for_review if row else False,
    }


def scoped_progress(user: User):
    return select(LessonProgress).join(Lesson).join(Module).where(
        LessonProgress.user_id == user.id, Lesson.is_active == True, module_scope(user)
    )


def scoped_mistakes(user: User):
    return select(MistakeBank).join(Question).join(Module).where(
        MistakeBank.user_id == user.id, MistakeBank.mastered_at.is_(None),
        Question.is_active == True, module_scope(user)
    )


@app.get("/api/progress")
def progress(request: Request, db: Session = Depends(get_db)):
    user = require_user(request, db)
    total_lessons = db.scalar(select(func.count()).select_from(Lesson).join(Module).where(Lesson.is_active == True, module_scope(user))) or 0
    progress_rows = db.scalars(scoped_progress(user)).all()
    completed = sum(1 for p in progress_rows if p.completed)
    mistakes = db.scalar(select(func.count()).select_from(scoped_mistakes(user).subquery())) or 0
    return {
        "total_lessons": total_lessons,
        "completed_lessons": completed,
        "percent_complete": round(completed / max(total_lessons, 1) * 100),
        "mistake_count": mistakes,
        "items": [lesson_progress_out(p, p.lesson_id) for p in progress_rows],
    }


@app.post("/api/lessons/{lesson_id}/progress")
def save_lesson_progress(lesson_id: int, payload: LessonProgressIn, request: Request, db: Session = Depends(get_db)):
    user = require_user(request, db)
    lesson = db.scalar(select(Lesson).join(Module).where(Lesson.id == lesson_id, Lesson.is_active == True, module_scope(user)))
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    row = db.scalar(select(LessonProgress).where(LessonProgress.user_id == user.id, LessonProgress.lesson_id == lesson.id))
    if not row:
        row = LessonProgress(user_id=user.id, lesson_id=lesson.id, completed=False, confidence=0, notes="", saved_for_review=False)
        db.add(row)
    # Omitted fields must not erase notes or change completion on a partial save.
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(row, field, value)
    db.commit()
    return {"ok": True, "progress": lesson_progress_out(row, lesson.id)}


@app.get("/api/mistakes")
def mistake_bank(request: Request, db: Session = Depends(get_db)):
    user = require_user(request, db)
    rows = db.scalars(scoped_mistakes(user).options(selectinload(MistakeBank.question).selectinload(Question.choices)).order_by(MistakeBank.times_missed.desc())).all()
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


class StudioIn(BaseModel):
    action: str
    module_slug: str

@app.post("/api/studio/generate")
def studio_generate(payload: StudioIn, request: Request, db: Session = Depends(get_db)):
    user = require_user(request, db)
    module = db.scalars(select(Module).where(Module.slug == payload.module_slug, module_scope(user))).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    lessons = db.scalars(select(Lesson).where(Lesson.module_id == module.id, Lesson.is_active == True).order_by(Lesson.sort_order)).all()
    terms = db.scalars(select(Term).where(Term.module_id == module.id).order_by(Term.term)).all()
    lesson_dicts = [{"title": l.title, "summary": l.summary or "", "body": l.body[:400] if l.body else "", "example": l.example or ""} for l in lessons]
    term_dicts = [{"term": t.term, "plain_english_definition": t.plain_english_definition or "", "exam_definition": t.exam_definition or "", "example": t.example or ""} for t in terms]
    from .tutor import generate_studio_content
    result = generate_studio_content(payload.action, module.title, term_dicts, lesson_dicts)
    return result


@app.get("/privacy")
def privacy_page():
    from fastapi.responses import HTMLResponse
    html = """<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Privacy Policy — WIT</title>
<style>body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;max-width:800px;margin:0 auto;padding:2rem;line-height:1.7;color:#333}h1{color:#1a1a1a}h2{color:#444;margin-top:2rem}a{color:#1a73e8}.back{display:inline-block;margin-bottom:2rem;color:#1a73e8;text-decoration:none}</style>
</head><body>
<a href="/" class="back">← Back to WIT</a>
<h1>Privacy Policy</h1>
<p><strong>Last updated: June 2026</strong></p>
<p>We Insure Things ("WIT") is committed to protecting your privacy. This policy explains what information we collect and how we use it.</p>
<h2>Information We Collect</h2>
<p>When you sign in with Google or Microsoft, we receive your name and email address. We store your study progress, quiz results, and lesson completions in our database to personalize your learning experience.</p>
<h2>How We Use Your Information</h2>
<p>We use your information solely to provide the WIT exam prep service — tracking your progress, personalizing study recommendations, and powering the Coverage Coach AI tutor. We do not sell your data. We do not share your data with third parties except as required to operate the service (OAuth providers for authentication).</p>
<h2>Coverage Coach AI</h2>
<p>Coverage Coach uses the Google Gemini API to answer your insurance questions. Your questions are sent to Google's API but are not associated with your personal identity — only the question text is transmitted, not your name or email.</p>
<h2>Data Storage</h2>
<p>Your data is stored on dedicated servers. We do not use third-party analytics or advertising services.</p>
<h2>Your Rights</h2>
<p>You may request deletion of your account and all associated data by emailing us at privacy@weinsurethings.com.</p>
<h2>Contact</h2>
<p>Questions? Email us at privacy@weinsurethings.com</p>
</body></html>"""
    return HTMLResponse(html)


@app.get("/terms")
def terms_page():
    from fastapi.responses import HTMLResponse
    html = """<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Terms of Service — WIT</title>
<style>body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;max-width:800px;margin:0 auto;padding:2rem;line-height:1.7;color:#333}h1{color:#1a1a1a}h2{color:#444;margin-top:2rem}a{color:#1a73e8}.back{display:inline-block;margin-bottom:2rem;color:#1a73e8;text-decoration:none}</style>
</head><body>
<a href="/" class="back">← Back to WIT</a>
<h1>Terms of Service</h1>
<p><strong>Last updated: June 2026</strong></p>
<p>By using We Insure Things ("WIT") you agree to these terms.</p>
<h2>The Service</h2>
<p>WIT provides free insurance licensing exam preparation materials. The service is provided as-is for educational purposes only. WIT is not an accredited educational institution and does not guarantee exam passage.</p>
<h2>Free Forever</h2>
<p>WIT is and will remain free. We will never charge for access to study materials, practice questions, or the Coverage Coach AI tutor.</p>
<h2>Acceptable Use</h2>
<p>You may use WIT for personal study purposes. You may not scrape, copy, or redistribute our content. You may not attempt to circumvent rate limits or abuse the Coverage Coach AI tutor.</p>
<h2>AI Tutor Disclaimer</h2>
<p>Coverage Coach is an AI assistant for exam prep only. It does not provide legal advice, binding insurance opinions, or claim determinations. Always consult a licensed professional for actual insurance matters.</p>
<h2>Intellectual Property</h2>
<p>Study content, questions, and materials on WIT are owned by We Insure Things. The WIT monster mascot and branding are proprietary.</p>
<h2>Limitation of Liability</h2>
<p>WIT is provided free of charge. To the maximum extent permitted by law, We Insure Things is not liable for any damages arising from use of the service.</p>
<h2>Contact</h2>
<p>Questions? Email us at legal@weinsurethings.com</p>
</body></html>"""
    return HTMLResponse(html)


@app.get("/api/dashboard")
def dashboard(request: Request, db: Session = Depends(get_db)):
    """Aggregated progress data for the dashboard view."""
    user = require_user(request, db)

    # ── Lesson completion ────────────────────────────────────────────
    total_lessons = (
        db.scalar(
            select(func.count()).select_from(Lesson)
            .join(Module, Module.id == Lesson.module_id)
            .where(Lesson.is_active == True, module_scope(user))
        ) or 0
    )
    progress_rows = db.scalars(
        scoped_progress(user)
    ).all()
    completed_ids = {p.lesson_id for p in progress_rows if p.completed}

    # ── Module breakdown + recommendations ──────────────────────────
    modules = db.scalars(
        select(Module)
        .where(module_scope(user))
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
    # Old attempts may mix courses/states. Calculate history from only the
    # answers belonging to the current selection instead of their stored score.
    attempt_query = (
        select(
            QuizAttempt.id,
            QuizAttempt.created_at,
            func.count(QuizAnswer.id).label("total"),
            func.sum(case((QuizAnswer.is_correct.is_(True), 1), else_=0)).label("correct"),
        )
        .join(QuizAnswer, QuizAnswer.attempt_id == QuizAttempt.id)
        .join(Question, Question.id == QuizAnswer.question_id)
        .join(Module, Module.id == Question.module_id)
        .where(QuizAttempt.user_id == user.id, Question.is_active == True, module_scope(user))
        .group_by(QuizAttempt.id, QuizAttempt.created_at)
    )
    total_attempts = db.scalar(select(func.count()).select_from(attempt_query.subquery())) or 0
    recent_attempts = [
        {"score": round(row.correct / row.total * 100), "total": row.total,
         "date": row.created_at.isoformat() if row.created_at else None}
        for row in db.execute(attempt_query.order_by(QuizAttempt.created_at.desc(), QuizAttempt.id.desc()).limit(10))
    ]
    avg_quiz = (
        round(sum(a["score"] for a in recent_attempts) / len(recent_attempts))
        if recent_attempts else 0
    )

    # ── Mistake bank ─────────────────────────────────────────────────
    mistake_count = (
        db.scalar(
            select(func.count()).select_from(scoped_mistakes(user).subquery())
        ) or 0
    )
    top_mistakes = db.scalars(
        scoped_mistakes(user)
        .options(selectinload(MistakeBank.question))
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
            "total_taken": total_attempts,
            "avg_score": avg_quiz,
            "recent": recent_attempts[:8],
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
