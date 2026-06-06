# P&C License Prep Academy — Server V2.1

This version moves the project toward the free public learning platform vision.

V2.1 focuses on three things:

1. **SSO-ready authentication** using Google, Microsoft, and Facebook OAuth.
2. **A real database-driven course system** for modules, lessons, terms, questions, answers, progress, quiz attempts, and mistake tracking.
3. **Coverage Coach**, a course-aware OpenAI/LLM study tutor with safe fallback mode.

The app remains free to the public. There are no payments, subscriptions, trials, or paywalls.

## What V2.1 includes

- FastAPI backend
- SQLAlchemy database layer
- SQLite for local development
- Postgres support through `DATABASE_URL`
- Google/Microsoft/Facebook OAuth route structure
- Development login route for local testing without OAuth keys
- Session-based logged-in user dashboard
- Database-backed modules
- Database-backed lessons
- Database-backed glossary/terms
- Database-backed questions and answer choices
- Lesson progress tied to users
- Quiz attempts and quiz answers
- Mistake bank with repeat-miss tracking
- Seed importer for course content
- Expanded generated question bank
- Coverage Coach tutor endpoint at `/api/tutor/ask`
- Frontend Coverage Coach screen
- Frontend that uses the API

## What V2.1 intentionally does not include yet

- Admin dashboard/content editor
- Question-polishing workflow
- State-specific content
- Certificates
- Team dashboards
- Payments

Those come after the auth, content, and tutor foundation is stable.

## Quick start

```bash
cd pc-license-prep-server-v2
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

## Local login

OAuth requires provider client IDs/secrets. For local development, use:

```text
/auth/dev-login
```

This creates or signs in a demo user. Disable it in production with:

```text
ENABLE_DEV_LOGIN=false
```

## Coverage Coach setup

Coverage Coach works in two modes:

1. `fallback` mode when no OpenAI key is configured.
2. `openai` mode when `OPENAI_API_KEY` is configured.

Environment variables:

```text
OPENAI_API_KEY=your-openai-api-key
OPENAI_MODEL=gpt-5.5-mini
OPENAI_MAX_OUTPUT_TOKENS=700
```

Tutor endpoint:

```text
POST /api/tutor/ask
```

Example body:

```json
{
  "message": "Explain the difference between a peril and a hazard, then quiz me."
}
```

Coverage Coach uses:

- matching lessons
- matching glossary terms
- the signed-in student's mistake bank
- guardrails against state-specific legal advice and binding coverage opinions

## OAuth setup

Set these environment variables when ready:

```text
APP_BASE_URL=https://your-domain.com
SESSION_SECRET=change-this-long-random-secret
DATABASE_URL=postgresql+psycopg://user:password@host:5432/dbname

GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=

MICROSOFT_CLIENT_ID=
MICROSOFT_CLIENT_SECRET=

FACEBOOK_CLIENT_ID=
FACEBOOK_CLIENT_SECRET=
```

OAuth callback URLs:

```text
https://your-domain.com/auth/callback/google
https://your-domain.com/auth/callback/microsoft
https://your-domain.com/auth/callback/facebook
```

## Content seed system

The default starter content lives in `app/course_seed.py`.

The generated question bank is expanded by `app/question_expander.py` and loaded by `app/content_loader.py`.

Current question-bank target:

```text
Baseline review: 1,050 questions
Scenario bank:     350 questions
Hard bank:         140 questions
Final simulation:  100 questions
Estimated total: 1,640 questions
```

## Production recommendation

For the public free launch, use Postgres. SQLite is fine locally but not ideal for public users.

Recommended next steps:

- Deploy V2.1 to a test environment
- Add OpenAI key in server environment variables
- Test Coverage Coach in fallback and OpenAI modes
- Build the question-polishing workflow
- Build the admin content editor
