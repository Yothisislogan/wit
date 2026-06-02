# API Reference — P&C License Prep Academy Server Starter

Base URL locally:

```text
http://127.0.0.1:8000
```

## Core endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Serves the frontend app when `frontend/index.html` exists. |
| GET | `/api/modules` | List modules. |
| GET | `/api/modules/{module_id}` | Get one module and its lessons. |
| GET | `/api/lessons/{lesson_id}` | Get one lesson. |
| GET | `/api/progress?learner_id=default` | Get progress summary and saved lesson records. |
| POST | `/api/progress` | Save lesson completion, confidence, and notes. |
| GET | `/api/questions?module_id=basics&limit=10` | Get quiz questions. |
| POST | `/api/questions/submit` | Submit quiz answers and save mistakes. |
| GET | `/api/mistakes?learner_id=default` | Review recent missed questions. |
| GET | `/api/flashcards` | Get flashcards generated from lesson terms. |
| GET | `/api/study-plan?learner_id=default` | Get readiness estimate and recommended lessons. |
| POST | `/api/tutor` | Ask Coverage Coach a general exam-prep question. |

## Submit progress example

```json
{
  "learner_id": "default",
  "lesson_id": "what-is-insurance",
  "completed": true,
  "confidence": 3,
  "note": "Insurance transfers financial risk.",
  "saved": false
}
```

## Submit quiz example

```json
{
  "learner_id": "default",
  "answers": {
    "q1": 0,
    "q2": 1
  }
}
```

## Coverage Coach example

```json
{
  "message": "What is the difference between a peril and a hazard?"
}
```

## Production upgrade path

This starter is intentionally simple. Recommended next API upgrades:

- user registration and login
- admin content editor
- larger external course seed file
- Postgres support
- Stripe or paid access
- OpenAI-backed tutor restricted to approved course content
- certificates of completion
- team reporting dashboard
