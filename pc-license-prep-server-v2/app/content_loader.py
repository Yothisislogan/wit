from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from .course_seed import DEFAULT_COURSE
from .course_seed_enrichment import enrich_course
from .models import Lesson, Module, Term


# Seed loader for course content.
def seed_course_if_empty(db: Session) -> None:
    enriched_course = enrich_course(DEFAULT_COURSE)
    load_course(db, enriched_course)


def load_course(db: Session, data: dict) -> None:
    for module_data in data.get("modules", []):
        module = db.scalar(select(Module).where(Module.slug == module_data["slug"]))
        if not module:
            module = Module(
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

        # Questions are seeded separately via scripts/load_real_questions.py.

    db.commit()
