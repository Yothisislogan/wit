# P&C License Prep Academy — Server Starter V1.1

This is a server-based starter for a general Property & Casualty licensing study app. It includes a FastAPI backend, SQLite progress tracking, mistake tracking, quiz endpoints, flashcards, a simple study plan endpoint, and a browser frontend.

The course remains **general Property & Casualty only**. No state-specific content is included.

## Current status

This is a working starter, not yet a full commercial LMS. The app currently uses anonymous learner IDs stored in the browser, not real student accounts.

## What is included now

- FastAPI backend
- SQLite database with automatic schema creation
- Anonymous learner progress tracking
- Lesson completion tracking
- Confidence tracking
- Lesson notes
- Quiz/question API
- Mistake bank API
- Adaptive study-plan style endpoint
- Flashcards with real definitions where available
- Simple keyword-matched Coverage Coach endpoint
- Static frontend served by FastAPI
- Dockerfile
- Render starter config

## What is not included yet

- student registration/login
- server-side sessions
- admin content editor
- payment/subscription access
- quiz-attempt history beyond saved mistakes
- true OpenAI-backed tutor
- certificates of completion
- team dashboard
- persistent Render disk setup or Postgres

## Quick start

```bash
cd pc-license-prep-server-v1
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Open:

```text
http://127.0.0.1:8000
```

API docs:

```text
http://127.0.0.1:8000/docs
```

Health check:

```text
http://127.0.0.1:8000/api/health
```

## Course seed data

The app now supports loading a course seed file from:

```text
app/data/course_seed.json
```

Expected format:

```json
{
  "modules": [],
  "questions": [],
  "flashcards": []
}
```

If no seed file exists, the app uses the smaller fallback course inside `app/main.py`.

## Environment variables

| Variable | Purpose |
|---|---|
| `DB_PATH` | SQLite database path. Defaults to `./pc_prep.db` inside this project folder. |
| `CORS_ORIGINS` | Comma-separated CORS origins. Defaults to `*`. |

## Render deployment note

The included `render.yaml` is a starter only. On Render's normal starter setup, the app filesystem may be ephemeral. That means SQLite learner progress can be lost on redeploy or restart unless you configure persistent disk or move to Postgres.

For production, move to Postgres and add real authentication before using this with paying students.

## Recommended next upgrades

1. Add real user accounts and login.
2. Move SQLite to Postgres for hosted persistence.
3. Add an admin content editor.
4. Expand to 500+ questions and full lesson content.
5. Connect Coverage Coach to an AI endpoint using only approved course content.
6. Add certificates of completion and team reporting.
