from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from .course_seed import DEFAULT_COURSE
from .models import AnswerChoice, Lesson, Module, Question, Term


def seed_course_if_empty(db: Session) -> None:
    """Load any missing seed modules.

    Despite the historical function name, this now works as an idempotent seed sync:
    it adds modules that do not already exist by slug. Existing modules are left
    untouched so student progress and edited content are not overwritten.
    """
    load_course(db, DEFAULT_COURSE)


def load_course(db: Session, data: dict) -> None:
    for module_data in data.get("modules", []):
        existing_module = db.scalar(select(Module).where(Module.slug == module_data["slug"]))
        if existing_module:
            continue

        module = Module(
            slug=module_data["slug"],
            title=module_data["title"],
            description=module_data.get("description", ""),
            sort_order=module_data.get("sort_order", 0),
            is_active=module_data.get("is_active", True),
        )
        db.add(module)
        db.flush()

        lessons_by_slug = {}
        for idx, lesson_data in enumerate(module_data.get("lessons", []), start=1):
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

        for term_data in module_data.get("terms", []):
            lesson = lessons_by_slug.get(term_data.get("lesson_slug", ""))
            db.add(Term(
                module_id=module.id,
                lesson_id=lesson.id if lesson else None,
                term=term_data["term"],
                plain_english_definition=term_data.get("plain_english_definition", ""),
                exam_definition=term_data.get("exam_definition", ""),
                example=term_data.get("example", ""),
            ))

        for question_data in module_data.get("questions", []):
            lesson = lessons_by_slug.get(question_data.get("lesson_slug", ""))
            question = Question(
                module_id=module.id,
                lesson_id=lesson.id if lesson else None,
                question_text=question_data["question_text"],
                question_type=question_data.get("question_type", "multiple_choice"),
                difficulty=question_data.get("difficulty", "standard"),
                explanation=question_data.get("explanation", ""),
                is_active=question_data.get("is_active", True),
            )
            db.add(question)
            db.flush()
            for idx, choice_data in enumerate(question_data.get("choices", []), start=1):
                db.add(AnswerChoice(
                    question_id=question.id,
                    choice_text=choice_data["choice_text"],
                    is_correct=choice_data.get("is_correct", False),
                    explanation=choice_data.get("explanation", ""),
                    sort_order=choice_data.get("sort_order", idx),
                ))
    db.commit()
