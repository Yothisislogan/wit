from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from sqlalchemy import or_, select
from sqlalchemy.orm import Session, selectinload

from .models import Lesson, MistakeBank, Question, Term, User
from .settings import settings

SYSTEM_PROMPT = """
You are Coverage Coach, a friendly Property & Casualty insurance licensing study tutor.

Rules:
- Use only the supplied course context and general P&C exam-prep knowledge.
- Keep answers state-neutral unless state-specific content is explicitly provided.
- Do not give legal advice, binding coverage advice, or claim determinations.
- Do not say a real-world claim is definitely covered.
- For coverage questions, explain that policy wording, conditions, and exclusions control.
- Prefer plain English, then include exam keywords.
- If the student asks for state law, claims advice, or coverage certainty, redirect to general exam concepts.
- End with one short practice question when useful.
""".strip()

FALLBACK_RESPONSE = """
Coverage Coach is not connected to the OpenAI API yet, but I can still help with the course context.

Study tip: identify whether the question is about property, liability, auto, homeowners, commercial lines, workers compensation, crime/bonds, contracts, or ethics. Then match the facts to the correct term, coverage part, condition, or exclusion.
""".strip()


@dataclass
class TutorContext:
    lessons: list[Lesson]
    terms: list[Term]
    mistakes: list[MistakeBank]


def _keywords(message: str) -> list[str]:
    stop = {
        "what", "when", "where", "why", "how", "does", "this", "that", "with", "from",
        "about", "insurance", "coverage", "policy", "please", "explain", "help", "mean",
    }
    words = [w.strip(".,?!:;()[]{}\"'").lower() for w in message.split()]
    return [w for w in words if len(w) > 3 and w not in stop][:8]


def get_tutor_context(db: Session, user: User, message: str, limit: int = 6) -> TutorContext:
    words = _keywords(message)
    lesson_stmt = select(Lesson).where(Lesson.is_active == True)
    term_stmt = select(Term)

    if words:
        lesson_filters = []
        term_filters = []
        for word in words:
            pattern = f"%{word}%"
            lesson_filters.extend([
                Lesson.title.ilike(pattern),
                Lesson.summary.ilike(pattern),
                Lesson.body.ilike(pattern),
                Lesson.example.ilike(pattern),
            ])
            term_filters.extend([
                Term.term.ilike(pattern),
                Term.plain_english_definition.ilike(pattern),
                Term.exam_definition.ilike(pattern),
                Term.example.ilike(pattern),
            ])
        lesson_stmt = lesson_stmt.where(or_(*lesson_filters))
        term_stmt = term_stmt.where(or_(*term_filters))

    lessons = list(db.scalars(lesson_stmt.order_by(Lesson.sort_order, Lesson.id).limit(limit)).all())
    terms = list(db.scalars(term_stmt.order_by(Term.term).limit(limit)).all())
    mistakes = list(
        db.scalars(
            select(MistakeBank)
            .options(selectinload(MistakeBank.question).selectinload(Question.choices))
            .where(MistakeBank.user_id == user.id)
            .order_by(MistakeBank.times_missed.desc())
            .limit(3)
        ).all()
    )
    return TutorContext(lessons=lessons, terms=terms, mistakes=mistakes)


def format_context(ctx: TutorContext) -> str:
    parts: list[str] = []
    if ctx.lessons:
        parts.append("Relevant lessons:")
        for lesson in ctx.lessons:
            parts.append(f"- {lesson.title}: {lesson.summary or lesson.body[:500]}")
            if lesson.example:
                parts.append(f"  Example: {lesson.example}")
    if ctx.terms:
        parts.append("Relevant glossary terms:")
        for term in ctx.terms:
            parts.append(f"- {term.term}: {term.exam_definition or term.plain_english_definition}")
            if term.example:
                parts.append(f"  Example: {term.example}")
    if ctx.mistakes:
        parts.append("Student weak areas from recent mistake bank:")
        for mistake in ctx.mistakes:
            if mistake.question:
                parts.append(f"- Missed {mistake.times_missed}x: {mistake.question.question_text[:280]}")
    return "\n".join(parts).strip()


def fallback_answer(ctx: TutorContext, message: str) -> dict[str, Any]:
    context = format_context(ctx)
    if context:
        answer = f"{FALLBACK_RESPONSE}\n\nRelevant course notes:\n{context[:1800]}"
    else:
        answer = FALLBACK_RESPONSE
    return {
        "answer": answer,
        "mode": "fallback",
        "model": None,
        "used_course_context": bool(context),
        "guardrail": "General P&C exam prep only. No state-specific legal, coverage, or claim advice.",
    }


def ask_coverage_coach(db: Session, user: User, message: str) -> dict[str, Any]:
    ctx = get_tutor_context(db, user, message)
    course_context = format_context(ctx)

    if not settings.openai_api_key:
        return fallback_answer(ctx, message)

    try:
        from openai import OpenAI
    except Exception:
        return fallback_answer(ctx, message)

    client = OpenAI(api_key=settings.openai_api_key)
    prompt = f"""
Student question:
{message}

Approved course context:
{course_context or 'No directly matching course context found. Use general state-neutral P&C exam-prep guidance only.'}

Answer as Coverage Coach. Be concise, helpful, and exam-focused.
""".strip()

    response = client.responses.create(
        model=settings.openai_model,
        instructions=SYSTEM_PROMPT,
        input=prompt,
        max_output_tokens=settings.openai_max_output_tokens,
    )
    answer = getattr(response, "output_text", None) or "Coverage Coach could not generate an answer. Try rephrasing the question."
    return {
        "answer": answer,
        "mode": "openai",
        "model": settings.openai_model,
        "used_course_context": bool(course_context),
        "guardrail": "General P&C exam prep only. No state-specific legal, coverage, or claim advice.",
    }
