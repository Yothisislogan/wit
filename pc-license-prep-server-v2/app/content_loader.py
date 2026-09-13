from __future__ import annotations

from sqlalchemy import select, text
from sqlalchemy.orm import Session

from .course_seed import DEFAULT_COURSE
from .course_seed_enrichment import enrich_course
from .models import AnswerChoice, Lesson, Module, Question, Term


# Seed loader for course content.
def seed_course_if_empty(db: Session) -> None:
    load_course(db, build_catalog())


def load_course(db: Session, data: dict) -> None:
    validate_catalog(data)
    # Serialize concurrent startup imports; release the lock with the transaction.
    if db.bind.dialect.name == "postgresql":
        db.execute(text("SELECT pg_advisory_xact_lock(87421063)"))
    elif db.bind.dialect.name == "sqlite" and not db.in_transaction():
        db.execute(text("BEGIN IMMEDIATE"))
    for module_data in data.get("modules", []):
        module = db.scalar(select(Module).where(Module.slug == module_data["slug"]))
        if not module:
            module = Module(
                course=module_data.get("course", "pc"),
                slug=module_data["slug"],
                title=module_data["title"],
                description=module_data.get("description", ""),
                sort_order=module_data.get("sort_order", 0),
                is_active=module_data.get("is_active", True),
            )
            db.add(module)
            db.flush()

        lessons_by_slug = {lesson.slug: lesson for lesson in db.scalars(select(Lesson).where(Lesson.module_id == module.id)).all()}
        for idx, lesson_data in enumerate(module_data.get("lessons", []), start=1):
            lesson = lessons_by_slug.get(lesson_data["slug"])
            if lesson:
                # Only fill blanks or replace exact bundled legacy stubs.
                for field in ("body", "summary", "example", "memory_tip", "audio_script"):
                    current = getattr(lesson, field)
                    original = lesson_data.get("_legacy", {}).get(field)
                    if not current or (original is not None and current == original):
                        setattr(lesson, field, lesson_data.get(field, current))
                continue
            lesson = Lesson(
                module_id=module.id,
                slug=lesson_data["slug"],
                title=lesson_data["title"],
                summary=lesson_data.get("summary", ""),
                body=lesson_data.get("body", ""),
                example=lesson_data.get("example", ""),
                memory_tip=lesson_data.get("memory_tip", ""),
                audio_script=lesson_data.get("audio_script", ""),
                estimated_minutes=lesson_data.get("estimated_minutes", 7),
                sort_order=lesson_data.get("sort_order", idx),
                is_active=lesson_data.get("is_active", True),
            )
            db.add(lesson)
            db.flush()
            lessons_by_slug[lesson.slug] = lesson

        existing_terms = {term.term.lower() for term in db.scalars(select(Term).where(Term.module_id == module.id)).all()}
        for term_data in module_data.get("terms", []):
            if term_data["term"].lower() in existing_terms:
                continue
            lesson = lessons_by_slug.get(term_data.get("lesson_slug", ""))
            db.add(Term(
                module_id=module.id,
                lesson_id=lesson.id if lesson else None,
                term=term_data["term"],
                plain_english_definition=term_data.get("plain_english_definition", ""),
                exam_definition=term_data.get("exam_definition", ""),
                example=term_data.get("example", ""),
            ))
            existing_terms.add(term_data["term"].lower())

        existing_questions = {q.question_text.strip(): q for q in db.scalars(
            select(Question).where(Question.module_id == module.id)).all()}
        for q_text, q_type, difficulty, explanation, choices in module_data.get("questions", []):
            question = existing_questions.get(q_text.strip())
            if question:
                # Keep IDs, edited answers, inactive flags, and student history intact.
                by_text = {c.choice_text: c for c in question.choices}
                if set(by_text) == {c[0] for c in choices} and all(
                    by_text[t].is_correct == correct for t, correct, _ in choices
                ):
                    if not question.explanation:
                        question.explanation = explanation
                    for choice_text, _, rationale in choices:
                        if not by_text[choice_text].explanation:
                            by_text[choice_text].explanation = rationale
                continue
            question = Question(module_id=module.id, question_text=q_text,
                                question_type=q_type, difficulty=difficulty,
                                explanation=explanation)
            db.add(question)
            db.flush()
            for order, (choice_text, correct, rationale) in enumerate(choices):
                db.add(AnswerChoice(question_id=question.id, choice_text=choice_text,
                                    is_correct=correct, explanation=rationale, sort_order=order))
            existing_questions[q_text.strip()] = question

    db.commit()



def build_catalog() -> dict:
    """Read bundled data, never run legacy database-writing entry points.

    State-law generators are deliberately excluded: their legal assertions have
    not been reviewed against current jurisdiction-specific sources.
    """
    from copy import deepcopy
    from importlib import import_module

    data = enrich_course(DEFAULT_COURSE)
    modules = {m["slug"]: m for m in data["modules"]}
    for module in modules.values():
        module["course"] = "pc"
        module["questions"] = []  # Ignore generated placeholder questions.
    for name, attribute in [("load_real_questions", "REAL_QUESTIONS"),
                            ("load_questions_batch2", "BATCH2_QUESTIONS"),
                            ("load_questions_batch3", "BATCH3_QUESTIONS")]:
        for slug, questions in getattr(import_module("scripts." + name), attribute).items():
            modules[slug]["questions"].extend(deepcopy(questions))
    for name in ("load_lesson_content", "load_lesson_content_batch2",
                 "load_lesson_content_batch3", "load_lesson_content_all_stubs"):
        content = import_module("scripts." + name).LESSON_CONTENT
        for module in modules.values():
            for lesson in module.get("lessons", []):
                if lesson["slug"] in content:
                    lesson.setdefault("_legacy", deepcopy(lesson))
                    lesson.update(zip(("body", "summary", "example", "memory_tip"), content[lesson["slug"]]))
    for name in ("lh_seed_part1", "lh_seed_part2", "lh_seed_part3"):
        for module in deepcopy(import_module("scripts." + name).MODULES):
            module["course"] = "lh"
            for term in module.get("terms", []):
                term["plain_english_definition"] = term.get("plain", "")
                term["exam_definition"] = term.get("exam", "")
            data["modules"].append(module)
    data["modules"].extend(deepcopy(import_module("scripts.gap_modules_seed").GAP_MODULES))
    return data


def validate_catalog(data: dict) -> None:
    """Validate the entire import before issuing any writes."""
    modules, lessons = set(), set()
    for module in data.get("modules", []):
        slug = module["slug"]
        if slug in modules or module.get("course", "pc") not in ("pc", "lh"):
            raise ValueError(f"Duplicate module or invalid course: {slug}")
        modules.add(slug)
        for lesson in module.get("lessons", []):
            if lesson["slug"] in lessons:
                raise ValueError(f"Duplicate lesson: {lesson['slug']}")
            lessons.add(lesson["slug"])
        seen = {}
        for question in module.get("questions", []):
            q_text, _, _, explanation, choices = question
            labels = [c[0].strip() for c in choices]
            if (not q_text.strip() or not explanation.strip() or len(choices) < 2
                    or not all(labels) or len(set(labels)) != len(labels)
                    or sum(c[1] is True for c in choices) != 1):
                raise ValueError(f"Invalid question in {slug}: {q_text}")
            key = q_text.strip()
            if key in seen and seen[key] != question:
                raise ValueError(f"Conflicting question in {slug}: {q_text}")
            seen[key] = question
