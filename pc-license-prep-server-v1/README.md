# P&C License Prep Academy — Server Version V1

This converts the static P&C licensing study app into a server-based web app with a REST API, SQLite database, student accounts, progress tracking, quiz attempts, mistakes, study plans, admin content tools, and an optional AI tutor endpoint.

The course remains **general Property & Casualty only**. No state-specific content is included.

## What is included

- FastAPI backend
- SQLite database with automatic schema creation
- Seeded course data
- Student registration and login
- Server-side sessions
- Lesson completion tracking
- Confidence tracking
- Saved lessons and notes
- Quiz, diagnostic, cram, and final exam APIs
- Mistake bank and drill mode
- Adaptive study plan endpoint
- Optional AI tutor endpoint
- Static frontend served by FastAPI

## Quick start

```bash
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

## Important note about course seed data

The original generated project package includes a large `app/data/course_seed.json` with the full seeded course content. If this repo upload is missing that large file, use the latest ZIP package from the build conversation or add your own `course_seed.json` at:

```text
app/data/course_seed.json
```

The server is designed so a fuller course bank can be dropped in without changing the API.

## Environment variables

Copy `.env.example` to `.env` if desired.

| Variable | Purpose |
|---|---|
| `DB_PATH` | SQLite database path |
| `SESSION_DAYS` | Login session duration |
| `CORS_ORIGINS` | Allowed CORS origins |
| `OPENAI_API_KEY` | Optional API key for AI tutor |
| `OPENAI_MODEL` | Optional AI model name |

## Deployment

The repo includes a Dockerfile and Render starter config. For production, consider moving from SQLite to Postgres, adding email verification, password reset, rate limiting, and paid access controls.