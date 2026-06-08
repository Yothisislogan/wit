from __future__ import annotations

import os
from typing import Any

import httpx
from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from .auth import require_user
from .database import get_db
from .models import Lesson, Module, Term
from .ratelimit import rate_limit
from .settings import settings
from .tutor import generate_studio_content

router = APIRouter()


def _ollama_host() -> str:
    base = settings.ollama_base_url.rstrip("/")
    return base[:-3] if base.endswith("/v1") else base


def ping_ollama() -> dict[str, Any]:
    try:
        with httpx.Client(timeout=3.0) as client:
            response = client.get(f"{_ollama_host()}/api/tags")
        if response.status_code != 200:
            return {"online": False, "model": settings.ollama_model, "detail": f"unexpected status {response.status_code}"}
        models = [m.get("name", "") for m in response.json().get("models", [])]
        model_root = settings.ollama_model.split(":")[0]
        pulled = settings.ollama_model in models or any(m.startswith(model_root) for m in models)
        if not pulled:
            return {"online": False, "model": settings.ollama_model, "detail": f"online but model {settings.ollama_model} is not pulled"}
        return {"online": True, "model": settings.ollama_model, "detail": "online"}
    except Exception as exc:
        return {"online": False, "model": settings.ollama_model, "detail": str(exc)[:160]}


class StudioRequest(BaseModel):
    action: str = Field(default="study_guide", max_length=40)
    module_slug: str = Field(default="", max_length=160)


@router.get("/api/coach/health")
def coach_health():
    openai_ready = bool(settings.openai_api_key and os.environ.get("OPENAI_MODEL"))
    if openai_ready:
        return {
            "coverage_coach_mode": "openai",
            "openai": {"online": True, "model": os.environ.get("OPENAI_MODEL"), "detail": "configured"},
            "ollama": ping_ollama(),
        }
    status = ping_ollama()
    return {"coverage_coach_mode": "ollama" if status["online"] else "fallback", "ollama": status}


@router.post("/api/studio/generate")
def studio_generate(body: StudioRequest, request: Request, db: Session = Depends(get_db)):
    user = require_user(request, db)
    rate_limit(f"studio:{user.id}", 5, 60)
    module_title = "P&C Insurance"
    terms_data: list[dict[str, str]] = []
    lessons_data: list[dict[str, str]] = []

    if body.module_slug:
        module_row = db.scalar(select(Module).where(Module.slug == body.module_slug))
        if module_row:
            module_title = module_row.title
            db_terms = db.scalars(select(Term).where(Term.module_id == module_row.id).limit(30)).all()
            db_lessons = db.scalars(select(Lesson).where(Lesson.module_id == module_row.id).limit(8)).all()
            terms_data = [
                {
                    "term": t.term,
                    "exam_definition": t.exam_definition or t.plain_english_definition,
                    "example": t.example or "",
                }
                for t in db_terms
            ]
            lessons_data = [
                {
                    "title": l.title,
                    "summary": l.summary or l.body[:220],
                }
                for l in db_lessons
            ]

    return generate_studio_content(body.action, module_title, terms_data, lessons_data)
