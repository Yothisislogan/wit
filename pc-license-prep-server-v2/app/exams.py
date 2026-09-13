"""Persistent timed general practice. No claim of state blueprint equivalence."""
import json
import random
from datetime import datetime, timedelta, timezone
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload

from .auth import require_user
from .database import get_db
from .models import Module, Question, TimedExam
from .study_scope import module_scope

router = APIRouter(prefix="/api/exams", tags=["timed practice"])
QUESTION_COUNT = 50
DURATION_MINUTES = 60


class SaveExam(BaseModel):
    revision: int = Field(ge=0)
    answers: dict[int, int] = Field(default_factory=dict, max_length=QUESTION_COUNT)
    flagged: list[int] = Field(default_factory=list, max_length=QUESTION_COUNT)


def utcnow():
    return datetime.now(timezone.utc)


def aware(value):
    return value.replace(tzinfo=timezone.utc) if value.tzinfo is None else value


def finish_if_expired(db, exam):
    if exam.completed_at is None and utcnow() >= aware(exam.deadline_at):
        changed = db.execute(update(TimedExam).where(
            TimedExam.id == exam.id, TimedExam.completed_at.is_(None),
            TimedExam.revision == exam.revision,
        ).values(completed_at=exam.deadline_at, active_slot=None, revision=exam.revision + 1))
        if changed.rowcount != 1:
            db.rollback()
            raise HTTPException(409, "Exam changed. Reload to get the saved version.")
        db.flush()
        db.refresh(exam)


def owned_exam(db, user, exam_id):
    exam = db.scalar(select(TimedExam).where(TimedExam.id == exam_id, TimedExam.user_id == user.id))
    if not exam:
        raise HTTPException(404, "Exam not found")
    finish_if_expired(db, exam)
    return exam


def exam_out(exam):
    snapshot = json.loads(exam.snapshot_json)
    answers = json.loads(exam.answers_json)
    complete = exam.completed_at is not None
    questions = []
    scores = {}
    correct_count = 0
    for q in snapshot:
        row = {k: q[k] for k in ("id", "question_text", "module_title")}
        row["choices"] = [{"id": c["id"], "choice_text": c["choice_text"]} for c in q["choices"]]
        if complete:
            correct = next(c for c in q["choices"] if c["is_correct"])
            selected = answers.get(str(q["id"]))
            is_correct = selected == correct["id"]
            correct_count += is_correct
            row.update(correct_choice_id=correct["id"], selected_choice_id=selected,
                       is_correct=is_correct, explanation=q["explanation"], choices=q["choices"])
            bucket = scores.setdefault(q["module_title"], {"correct": 0, "total": 0})
            bucket["total"] += 1
            bucket["correct"] += is_correct
        questions.append(row)
    return {"id": exam.id, "course": exam.course, "mode": "general_timed_practice",
            "status": "completed" if complete else "in_progress", "revision": exam.revision,
            "started_at": aware(exam.started_at).isoformat(), "deadline_at": aware(exam.deadline_at).isoformat(),
            "server_now": utcnow().isoformat(), "answers": answers, "flagged": json.loads(exam.flags_json),
            "questions": questions, "total_questions": len(questions),
            "result": {"correct": correct_count, "percent": round(100 * correct_count / len(questions)),
                       "module_scores": scores} if complete else None,
            "notice": "General course practice: 50 questions, 60 minutes. No state-law questions or official exam weighting. Scores are raw practice percentages, not licensing results."}


@router.get("/active")
def active_exam(request: Request, db: Session = Depends(get_db)):
    user = require_user(request, db)
    exam = db.scalar(select(TimedExam).where(TimedExam.user_id == user.id, TimedExam.active_slot == 1))
    if exam:
        finish_if_expired(db, exam)
    else:
        exam = db.scalar(select(TimedExam).where(TimedExam.user_id == user.id).order_by(TimedExam.started_at.desc()).limit(1))
    return {"exam": exam_out(exam) if exam else None}


@router.post("")
def start_exam(request: Request, db: Session = Depends(get_db)):
    user = require_user(request, db)
    active = db.scalar(select(TimedExam).where(TimedExam.user_id == user.id, TimedExam.active_slot == 1))
    if active:
        finish_if_expired(db, active)
        return exam_out(active)
    bank = db.scalars(select(Question).join(Module).where(
        Question.is_active.is_(True), module_scope(user), ~Module.slug.like("state-law-%")
    ).options(selectinload(Question.choices), selectinload(Question.module))).all()
    groups = {}
    seen = set()
    for q in bank:
        labels = [c.choice_text.strip() for c in q.choices]
        identity = q.question_text.strip().casefold()
        if (identity in seen or len(labels) < 2 or len(set(labels)) != len(labels)
                or sum(c.is_correct for c in q.choices) != 1):
            continue
        seen.add(identity)
        groups.setdefault(q.module_id, []).append(q)
    available = sum(map(len, groups.values()))
    if available < QUESTION_COUNT:
        raise HTTPException(409, f"Timed practice needs {QUESTION_COUNT} unique valid questions; this course has {available}.")
    # Round-robin shuffled modules gives breadth without claiming official weights.
    buckets = list(groups.values())
    random.shuffle(buckets)
    for bucket in buckets:
        random.shuffle(bucket)
    selected = []
    while len(selected) < QUESTION_COUNT:
        for bucket in buckets:
            if bucket and len(selected) < QUESTION_COUNT:
                selected.append(bucket.pop())
    random.shuffle(selected)
    snapshot = []
    for q in selected:
        choices = [{"id": c.id, "choice_text": c.choice_text, "is_correct": c.is_correct,
                    "explanation": c.explanation} for c in q.choices]
        random.shuffle(choices)
        snapshot.append({"id": q.id, "question_text": q.question_text, "module_title": q.module.title,
                         "explanation": q.explanation, "choices": choices})
    now = utcnow()
    exam = TimedExam(id=str(uuid4()), user_id=user.id, course=user.course or "pc", started_at=now,
                     deadline_at=now + timedelta(minutes=DURATION_MINUTES), snapshot_json=json.dumps(snapshot))
    db.add(exam)
    try:
        db.flush()
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, "An exam was started in another tab. Resume the active exam.")
    return exam_out(exam)


@router.get("/{exam_id}")
def get_exam(exam_id: str, request: Request, db: Session = Depends(get_db)):
    return exam_out(owned_exam(db, require_user(request, db), exam_id))


def save(db, exam, payload, finish=False):
    if exam.completed_at is not None:
        return exam_out(exam)  # Retries and late requests cannot change results.
    questions = {q["id"]: q for q in json.loads(exam.snapshot_json)}
    for question_id, choice_id in payload.answers.items():
        if question_id not in questions or choice_id not in {c["id"] for c in questions[question_id]["choices"]}:
            raise HTTPException(422, "Answer does not belong to this exam")
    if any(q not in questions for q in payload.flagged):
        raise HTTPException(422, "Review flag does not belong to this exam")
    answers = json.loads(exam.answers_json)
    answers.update({str(k): v for k, v in payload.answers.items()})
    values = {"answers_json": json.dumps(answers), "flags_json": json.dumps(sorted(set(payload.flagged))),
              "revision": payload.revision + 1}
    if finish:
        values.update(completed_at=utcnow(), active_slot=None)
    changed = db.execute(update(TimedExam).where(
        TimedExam.id == exam.id, TimedExam.revision == payload.revision,
        TimedExam.completed_at.is_(None), TimedExam.deadline_at > utcnow(),
    ).values(**values).execution_options(synchronize_session=False))
    if changed.rowcount != 1:
        db.rollback()
        db.refresh(exam)
        finish_if_expired(db, exam)
        if exam.completed_at is not None:
            return exam_out(exam)
        raise HTTPException(409, "Exam changed in another tab. Reload to get the saved version.")
    db.flush()
    db.refresh(exam)
    return exam_out(exam)


@router.put("/{exam_id}/answers")
def save_answers(exam_id: str, payload: SaveExam, request: Request, db: Session = Depends(get_db)):
    return save(db, owned_exam(db, require_user(request, db), exam_id), payload)


@router.post("/{exam_id}/submit")
def submit_exam(exam_id: str, payload: SaveExam, request: Request, db: Session = Depends(get_db)):
    return save(db, owned_exam(db, require_user(request, db), exam_id), payload, finish=True)
