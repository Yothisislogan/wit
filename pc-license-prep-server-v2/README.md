# P&C License Prep Academy — Server V2

This version moves the project toward the free public learning platform vision.

V2 focuses on two things:

1. **SSO-ready authentication** using Google, Microsoft, and Facebook OAuth.
2. **A real database-driven course system** for modules, lessons, terms, questions, answers, progress, quiz attempts, and mistake tracking.

The app remains free to the public. There are no payments, subscriptions, trials, or paywalls.

## What V2 includes

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
- Frontend that uses the API

## What V2 intentionally does not include yet

- Admin dashboard/content editor
- AI tutor
- State-specific content
- Certificates
- Team dashboards
- Payments

Those come after the auth and content foundation is stable.

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

Later, larger content can be imported from JSON using the same shape:

```json
{
  "modules": [
    {
      "slug": "insurance-basics",
      "title": "Insurance Basics",
      "description": "Foundational insurance concepts.",
      "sort_order": 1,
      "lessons": [],
      "terms": [],
      "questions": []
    }
  ]
}
```

## Production recommendation

For the public free launch, use Postgres. SQLite is fine locally but not ideal for public users.

Recommended next step after this version:

- Build the admin content editor
- Expand the seed content to 75+ lessons and 500+ questions
- Add the AI tutor only after the course database has enough approved content
