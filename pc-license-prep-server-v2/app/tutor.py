from __future__ import annotations

import json
import os
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
Coverage Coach is in study mode. The live model is not reachable yet, so I am answering from built-in course notes and general state-neutral P&C exam-prep rules.
""".strip()

STATIC_TOPICS = {
    "inland marine": {
        "term": "Inland Marine",
        "answer": "Inland marine insurance is property coverage for movable property, property in transit, or property that is not well covered by a standard fixed-location property policy. It often covers items such as contractors equipment, tools, installation materials, valuable papers, accounts receivable, fine arts, or property being transported.",
        "exam": "Exam keyword: movable property / property in transit / specialized property floaters.",
        "example": "Example: A contractor's tools and equipment that move from jobsite to jobsite are commonly an inland marine exposure.",
    },
    "peril": {
        "term": "Peril",
        "answer": "A peril is the cause of loss, such as fire, theft, wind, hail, or collision.",
        "exam": "Exam keyword: cause of loss.",
        "example": "If lightning damages a building, lightning is the peril.",
    },
    "hazard": {
        "term": "Hazard",
        "answer": "A hazard is a condition that increases the chance or severity of a loss.",
        "exam": "Exam keyword: increases probability or severity.",
        "example": "Faulty wiring is a physical hazard because it increases the chance of fire.",
    },
    "deductible": {
        "term": "Deductible",
        "answer": "A deductible is the insured's share of a covered loss before the insurer pays.",
        "exam": "Exam keyword: insured retention per loss.",
        "example": "If a covered loss is $5,000 and the deductible is $1,000, the insurer generally pays $4,000, subject to policy terms.",
    },
    "coinsurance": {
        "term": "Coinsurance",
        "answer": "Coinsurance is an insurance-to-value requirement. If the insured does not carry enough insurance compared with the required percentage, a partial-loss penalty may apply.",
        "exam": "Exam keyword: insurance to value / underinsurance penalty.",
        "example": "An 80% coinsurance clause requires insurance equal to at least 80% of the property's value to avoid penalty.",
    },
}


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


def _call_openai(system: str, user_prompt: str) -> str:
    api_key = settings.openai_api_key
    model = os.environ.get("OPENAI_MODEL", "")
    if not api_key or not model:
        raise RuntimeError("OpenAI is not configured")
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user_prompt},
        ],
        "max_tokens": settings.openai_max_output_tokens,
    }
    with httpx.Client(timeout=90.0) as client:
        response = client.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json=payload,
        )
        response.raise_for_status()
    data = response.json()
    return _strip_think(data["choices"][0]["message"]["content"])


def _call_best_model(system: str, user_prompt: str) -> tuple[str, str, str | None]:
    if settings.openai_api_key and os.environ.get("OPENAI_MODEL"):
        try:
            return _call_openai(system, user_prompt), "openai", os.environ.get("OPENAI_MODEL")
        except Exception:
            pass
    try:
        return _call_ollama(system, user_prompt), "ollama", settings.ollama_model
    except Exception as exc:
        raise RuntimeError(str(exc)) from exc


def _static_topic_answer(message: str) -> str:
    lower = message.lower()
    for key, item in STATIC_TOPICS.items():
        if key in lower:
            return f"{item['term']}: {item['answer']}\n\n{item['exam']}\n\n{item['example']}\n\nPractice check: Which phrase best describes {item['term']} for the exam?"
    return ""


def _fallback_answer(ctx: TutorContext, message: str = "") -> dict[str, Any]:
    context = format_context(ctx)
    topical = _static_topic_answer(message)
    if topical:
        answer = topical
    elif context:
        answer = f"{FALLBACK_RESPONSE}\n\nRelevant course notes:\n{context[:1800]}"
    else:
        answer = f"{FALLBACK_RESPONSE}\n\nAsk about a specific term like peril, hazard, deductible, coinsurance, inland marine, homeowners, CGL, or business auto and I can still give a useful study answer."
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
        answer, mode, model = _call_best_model(SYSTEM_PROMPT, prompt)
        return {"answer": answer, "mode": mode, "model": model, "used_course_context": bool(course_context), "guardrail": GUARDRAIL}
    except Exception:
        return _fallback_answer(ctx, message)


def _fallback_quiz(module_title: str, terms: list[dict], lessons: list[dict]) -> dict[str, Any]:
    questions: list[dict[str, Any]] = []
    source_terms = terms[:5] or [
        {"term": "Peril", "exam_definition": "A cause of loss.", "example": "Fire damages a building."},
        {"term": "Hazard", "exam_definition": "A condition that increases chance or severity of loss.", "example": "Faulty wiring."},
        {"term": "Deductible", "exam_definition": "The insured share of a covered loss.", "example": "A $1,000 deductible."},
    ]
    for idx, term in enumerate(source_terms, start=1):
        questions.append({
            "q": f"Which answer best describes {term.get('term', 'this term')}?",
            "choices": [
                term.get("exam_definition", "The correct exam definition."),
                "A guarantee that every claim will be paid.",
                "A state-specific producer appointment rule.",
                "A type of life insurance settlement option.",
            ],
            "correct": 0,
            "explanation": term.get("example") or "Match the term to its exam definition.",
        })
    return {"action": "practice_quiz", "module": module_title, "questions": questions[:5]}


def _fallback_studio_content(action: str, module_title: str, terms: list[dict], lessons: list[dict]) -> dict[str, Any]:
    if action == "cram_sheet":
        return {"action": action, "module": module_title, "terms": terms}
    if action == "practice_quiz":
        return _fallback_quiz(module_title, terms, lessons)

    lesson_lines = [f"- {l.get('title', 'Lesson')}: {l.get('summary', '')}" for l in lessons[:6]]
    term_lines = [f"- {t.get('term', 'Term')}: {t.get('exam_definition', '')}" for t in terms[:10]]
    if not lesson_lines:
        lesson_lines = ["- Start with risk, peril, hazard, contract parts, property valuation, and liability basics."]
    if not term_lines:
        term_lines = ["- Peril: cause of loss.", "- Hazard: increases chance or severity of loss.", "- Deductible: insured share of a covered loss."]

    if action == "concept_map":
        content = f"{module_title} concept map\n\nCore lessons\n" + "\n".join(lesson_lines) + "\n\nKey terms\n" + "\n".join(term_lines) + "\n\nExam method: identify the line of insurance, identify the coverage part, look for exclusions/conditions, then choose the best answer."
    else:
        content = f"{module_title} study guide\n\nWhat to know\n" + "\n".join(lesson_lines) + "\n\nKey terms\n" + "\n".join(term_lines) + "\n\nMemory tip: do not assume coverage. Match the facts to policy wording, conditions, and exclusions."
    return {"action": action, "module": module_title, "content": content, "mode": "deterministic_fallback"}


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
        text, mode, model = _call_best_model(SYSTEM_PROMPT, f"{instructions}\n\nCourse context JSON:\n{json.dumps(context, ensure_ascii=False)}")
        if action == "practice_quiz":
            try:
                parsed = json.loads(text)
                if isinstance(parsed, dict) and isinstance(parsed.get("questions"), list):
                    return {"action": action, "module": module_title, "questions": parsed["questions"][:5], "mode": mode, "model": model}
            except Exception:
                pass
        return {"action": action, "module": module_title, "content": text, "mode": mode, "model": model}
    except Exception:
        return _fallback_studio_content(action, module_title, terms, lessons)
