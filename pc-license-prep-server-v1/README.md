# P&C License Prep Academy Server Starter V1

Lightweight FastAPI starter for the Property and Casualty licensing study app.

V1 is a simple reference build. The newer public platform work is in pc-license-prep-server-v2.

## Quick start

```bash
cd pc-license-prep-server-v1
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Open http://127.0.0.1:8000

API docs are at http://127.0.0.1:8000/docs
