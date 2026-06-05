# API Reference — P&C License Prep Academy Server Starter V1.1

Base URL locally:

```text
http://127.0.0.1:8000
```

## Core endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Serves the frontend app when `frontend/index.html` exists. |
| GET | `/api/health` | Health check plus module/question counts and seed-file status. |
| GET | `/api/modules` | List modules. |
| GET | `/api/modules/{module_id}` | Get one module and its lessons. |
| GET | `/api/lessons/{lesson_id}` | Get one lesson. |
| GET | `/api/progress?learner_id=default` | Get progress summary and saved lesson records. |
| POST | `/api/progress` | Save lesson completion, confidence, and notes. |
| GET | `/api/questions?module_id=basics&limit=10` | Get quiz questions. Limit is capped from 1 to 50. |
| POST | `/api/questions/submit` | Submit up to 50 quiz answers and save mistakes. |
| GET | `/api/mistakes?learner_id=default&limit=50` | Review recent missed questions. Limit is capped from 1 to 100. |
| GET | `/api/flashcards` | Get seeded flashcards, or generated flashcards from lesson terms. |
| GET | `/api/study-plan?learner_id=default` | Get readiness estimate and recommended lessons. |
| POST | `/api/tutor` | Ask the keyword-matched Coverage Coach a general exam-prep question. |

## Health response example

```json
{
  "ok": true,
  "modules": 10,
  "questions": 10,
  "seed_file_loaded": false
}
```

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

## Course seed file format

Place this file at `app/data/course_seed.json`:

```json
{
  "modules": [
    {
      "id": "basics",
      "title": "Insurance Basics",
      "lessons": [
        {
          "id": "what-is-insurance",
          "title": "What Is Insurance?",
          "body": "Lesson body text...",
          "terms": ["risk", "premium"]
        }
      ]
    }
  ],
  "questions": [
    {
      "id": "q1",
      "module_id": "basics",
      "question": "What is a peril?",
      "choices": ["The cause of loss", "The premium", "The insured", "The limit"],
      "answer": 0,
      "explanation": "A peril is the cause of loss."
    }
  ],
  "flashcards": [
    {
      "term": "Peril",
      "definition": "The cause of loss.",
      "module": "Insurance Basics"
    }
  ]
}
```

## Coverage Coach example

```json
{
  "message": "What is the difference between a peril and a hazard?"
}
```

Note: Coverage Coach in this version is keyword-matched. It is not an AI model yet.

## Production upgrade path

This starter is intentionally simple. Recommended next API upgrades:

- user registration and login
- admin content editor
- full course seed file with 500+ questions
- Postgres support
- Stripe or paid access
- OpenAI-backed tutor restricted to approved course content
- certificates of completion
- team reporting dashboard
