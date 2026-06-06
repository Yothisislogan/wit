from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any

import httpx
from sqlalchemy import or_, select
from sqlalchemy.orm import Session, selectinload

from .models import Lesson, MistakeBank, Question, Term, User
from .settings import settings

SYSTEM_PROMPT = """
You are Coverage Coach, a friendly Property & Casualty insurance licensing study tutor.
Use the supplied course context when available. Keep answers state-neutral. Do not give legal advice, binding coverage opinions, or claim determinations. Explain that policy wording, conditions, and exclusions control. Prefer plain English, then exam keywords. End with one short practice question when useful.
""".strip()

GUARDRAIL = "General P&C exam prep only. No state-specific legal, coverage, or claim advice."

FALLBACK_RESPONSE = """
Coverage Coach is in fallback mode. The course is still usable, but the local model is not reachable yet.

Study tip: identify whether the question is about property, liability, auto, homeowners, commercial lines, workers compensation, crime/bonds, contracts, or ethics. Then match the facts to the correct term, coverage part, condition, or exclusion.
""".strip()


@dataclass
class TutorContext:
    lessons: list[Lesson]
    terms: list[Term]
    mistakes: list[MistakeBank]


def _keywords(message: str) -> list[str]:
    stop = {"what", "when", "where", "why", "how", "does", "this", "that", "with", "from", "about", "insurance", "coverage", "policy", "please", "explain", "help", "mean"}
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
            pat = f"%{word}%"
            lesson_filters.extend([Lesson.title.ilike(pat), Lesson.summary.ilike(pat), Lesson.body.ilike(pat), Lesson.example.ilike(pat)])
            term_filters.extend([Term.term.ilike(pat), Term.plain_english_definition.ilike(pat), Term.exam_definition.ilike(pat), Term.example.ilike(pat)])
        lesson_stmt = lesson_stmt.where(or_(*lesson_filters))
        term_stmt = term_stmt.where(or_(*term_filters))
    lessons = list(db.scalars(lesson_stmt.order_by(Lesson.sort_order, Lesson.id).limit(limit)).all())
    terms = list(db.scalars(term_stmt.order_by(Term.term).limit(limit)).all())
    mistakes = list(db.scalars(select(MistakeBank).options(selectinload(MistakeBank.question).selectinload(Question.choices)).where(MistakeBank.user_id == user.id).order_by(MistakeBank.times_missed.desc()).limit(3)).all())
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


def _strip_think(text: str) -> str:
    return re.sub(r"<think>.*?</think>", "", text or "", flags=re.DOTALL).strip()


def _call_ollama(system: str, user_prompt: str) -> str:
    url = settings.ollama_base_url.rstrip("/") + "/chat/completions"
    payload = {
        "model": settings.ollama_model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user_prompt},
        ],
        "max_tokens": settings.ollama_max_tokens,
        "stream": False,
    }
    with httpx.Client(timeout=90.0) as client:
        response = client.post(url, json=payload)
        response.raise_for_status()
    data = response.json()
    return _strip_think(data["choices"][0]["message"]["content"])


def _fallback_answer(ctx: TutorContext) -> dict[str, Any]:
    context = format_context(ctx)
    answer = FALLBACK_RESPONSE
    if context:
        answer = f"{FALLBACK_RESPONSE}\n\nRelevant course notes:\n{context[:1800]}"
    return {"answer": answer, "mode": "fallback", "model": None, "used_course_context": bool(context), "guardrail": GUARDRAIL}


def ask_coverage_coach(db: Session, user: User, message: str) -> dict[str, Any]:
    ctx = get_tutor_context(db, user, message)
    course_context = format_context(ctx)
    prompt = f"""
Student question:
{message}

Approved course context:
{course_context or 'No directly matching course context found. Use general state-neutral P&C exam-prep guidance only.'}

Answer as Coverage Coach. Be concise, helpful, and exam-focused.
""".strip()
    try:
        answer = _call_ollama(SYSTEM_PROMPT, prompt)
        return {"answer": answer, "mode": "ollama", "model": settings.ollama_model, "used_course_context": bool(course_context), "guardrail": GUARDRAIL}
    except Exception:
        return _fallback_answer(ctx)


def generate_studio_content(action: str, module_title: str, terms: list[dict], lessons: list[dict]) -> dict[str, Any]:
    context = {
        "module": module_title,
        "lessons": lessons[:8],
        "terms": terms[:25],
    }
    if action == "cram_sheet":
        return {"action": action, "module": module_title, "terms": terms}

    instructions = {
        "study_guide": "Create a concise study guide with key ideas, memory tips, and 5 review bullets.",
        "practice_quiz": "Create exactly 5 multiple-choice questions. Return JSON with a questions array; each item has q, choices, correct, explanation.",
        "concept_map": "Create a text-based concept map connecting the module's lessons and terms.",
    }.get(action, "Create a useful study output for this module.")

    try:
        text = _call_ollama(SYSTEM_PROMPT, f"{instructions}\n\nCourse context JSON:\n{json.dumps(context, ensure_ascii=False)}")
        if action == "practice_quiz":
            try:
                parsed = json.loads(text)
                if isinstance(parsed, dict) and isinstance(parsed.get("questions"), list):
                    return {"action": action, "module": module_title, "questions": parsed["questions"][:5]}
            except Exception:
                pass
        return {"action": action, "module": module_title, "content": text}
    except Exception as exc:
        return {"action": action, "module": module_title, "error": str(exc)[:180]}
