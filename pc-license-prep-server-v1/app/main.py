from __future__ import annotations

import json
import os
import random
import sqlite3
import time
from contextlib import asynccontextmanager, contextmanager
from pathlib import Path
from typing import Any, Iterator

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

ROOT_DIR = Path(__file__).resolve().parent.parent
APP_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = ROOT_DIR / "frontend"
DATA_DIR = APP_DIR / "data"
SEED_PATH = DATA_DIR / "course_seed.json"
DB_PATH = Path(os.environ.get("DB_PATH", str(ROOT_DIR / "pc_prep.db")))

FALLBACK_MODULES: list[dict[str, Any]] = [
    {"id":"basics","title":"Insurance Basics","lessons":[
        {"id":"what-is-insurance","title":"What Is Insurance?","body":"Insurance transfers the financial cost of certain losses from an individual or business to an insurer. The insured pays premium; the insurer promises to pay covered losses according to the policy.","terms":["risk","premium","loss","insurer","insured"]},
        {"id":"risk-peril-hazard","title":"Risk, Peril, and Hazard","body":"Risk is the chance of loss. A peril is the cause of loss, such as fire or theft. A hazard is a condition that increases the chance or severity of loss.","terms":["risk","peril","hazard","moral hazard","physical hazard"]},
        {"id":"risk-management","title":"Risk Management Methods","body":"People manage risk by avoiding, reducing, retaining, sharing, or transferring it. Insurance is a transfer method because the insurer takes on covered financial risk.","terms":["avoidance","reduction","retention","sharing","transfer"]}
    ]},
    {"id":"contracts","title":"Insurance Contracts","lessons":[
        {"id":"contract-parts","title":"Parts of an Insurance Policy","body":"Most policies include declarations, insuring agreement, conditions, exclusions, and endorsements. Endorsements can add, remove, or change coverage.","terms":["declarations","insuring agreement","conditions","exclusions","endorsement"]},
        {"id":"contract-traits","title":"Characteristics of Insurance Contracts","body":"Insurance contracts are usually contracts of adhesion, aleatory, conditional, unilateral, and personal. The policy is interpreted based on its written terms.","terms":["adhesion","aleatory","conditional","unilateral","personal"]}
    ]},
    {"id":"property","title":"Property Insurance Fundamentals","lessons":[
        {"id":"property-values","title":"Valuation Basics","body":"Replacement cost pays to replace damaged property without depreciation, subject to policy terms. Actual cash value usually means replacement cost minus depreciation.","terms":["replacement cost","actual cash value","depreciation","deductible","coinsurance"]},
        {"id":"direct-indirect-loss","title":"Direct and Indirect Loss","body":"A direct loss is physical damage to covered property. An indirect loss is a financial result of that damage, such as loss of income or extra living expense.","terms":["direct loss","indirect loss","loss of use","business income"]}
    ]},
    {"id":"casualty","title":"Casualty Insurance Fundamentals","lessons":[
        {"id":"liability-basics","title":"Liability Basics","body":"Casualty insurance often deals with legal liability to others. Common liability losses include bodily injury, property damage, personal injury, and advertising injury.","terms":["bodily injury","property damage","personal injury","advertising injury","negligence"]},
        {"id":"limits","title":"Limits and Defense","body":"Liability policies use limits to cap what the insurer will pay. Many liability policies also provide defense for covered suits, subject to policy terms.","terms":["limit","aggregate","occurrence","defense costs","damages"]}
    ]},
    {"id":"auto","title":"Personal Auto Insurance","lessons":[
        {"id":"auto-liability","title":"Auto Liability","body":"Auto liability helps pay for bodily injury or property damage the insured becomes legally responsible for because of an auto accident.","terms":["liability","split limits","combined single limit","permissive use"]},
        {"id":"auto-physical-damage","title":"Auto Physical Damage","body":"Collision covers upset or impact with another object. Other than collision, often called comprehensive, covers many non-collision losses such as theft, fire, or hail.","terms":["collision","comprehensive","deductible","covered auto"]}
    ]},
    {"id":"homeowners","title":"Homeowners Insurance","lessons":[
        {"id":"home-coverages","title":"Homeowners Coverages","body":"Common homeowners coverages include dwelling, other structures, personal property, loss of use, personal liability, and medical payments to others.","terms":["Coverage A","Coverage B","Coverage C","Coverage D","Coverage E","Coverage F"]}
    ]},
    {"id":"commercial","title":"Commercial Lines Overview","lessons":[
        {"id":"commercial-property","title":"Commercial Property","body":"Commercial property can cover buildings, business personal property, and property of others. Business income and extra expense address income-related losses after covered damage.","terms":["building","business personal property","business income","extra expense"]},
        {"id":"cgl","title":"Commercial General Liability","body":"CGL coverage commonly includes Coverage A for bodily injury and property damage, Coverage B for personal and advertising injury, and Coverage C for medical payments.","terms":["CGL","premises","operations","products-completed operations","medical payments"]}
    ]},
    {"id":"workers-comp","title":"Workers Compensation","lessons":[
        {"id":"wc-purpose","title":"Workers Compensation Purpose","body":"Workers compensation generally provides medical, disability, and death benefits for work-related injuries or disease, without requiring the injured worker to prove employer negligence.","terms":["medical benefits","disability benefits","death benefits","exclusive remedy","employers liability"]}
    ]},
    {"id":"ethics","title":"Ethics and Producer Responsibilities","lessons":[
        {"id":"producer-ethics","title":"Producer Ethics","body":"Producers should communicate honestly, document clearly, avoid misrepresentation, handle premium responsibly, and stay within their authority.","terms":["misrepresentation","rebating","twisting","fiduciary duty","binding authority"]}
    ]},
    {"id":"exam-prep","title":"Exam Prep","lessons":[
        {"id":"exam-strategy","title":"Exam Strategy","body":"Read each question carefully, identify the coverage type, eliminate wrong answers, and watch for words like except, always, never, and only.","terms":["keyword recognition","elimination","scenario question","review"]}
    ]}
]

FALLBACK_QUESTIONS = [
    {"id":"q1","module_id":"basics","question":"What is a peril?","choices":["The cause of loss","The amount paid for coverage","The person insured","The policy limit"],"answer":0,"explanation":"A peril is the cause of loss, such as fire, theft, or wind."},
    {"id":"q2","module_id":"basics","question":"Which risk management method best describes buying insurance?","choices":["Avoidance","Transfer","Retention","Elimination"],"answer":1,"explanation":"Insurance transfers covered financial risk to the insurer."},
    {"id":"q3","module_id":"contracts","question":"Which policy section lists who is insured and the limits?","choices":["Declarations","Exclusions","Conditions","Definitions"],"answer":0,"explanation":"The declarations page summarizes named insured, limits, dates, and other key information."},
    {"id":"q4","module_id":"property","question":"Actual cash value is commonly described as replacement cost minus what?","choices":["Premium","Depreciation","Deductible only","Coinsurance penalty only"],"answer":1,"explanation":"ACV is commonly replacement cost less depreciation, subject to policy terms."},
    {"id":"q5","module_id":"casualty","question":"Liability coverage is usually what type of coverage?","choices":["First-party only","Third-party","Life insurance","Health insurance"],"answer":1,"explanation":"Liability coverage responds to claims made by others against the insured."},
    {"id":"q6","module_id":"auto","question":"Collision coverage generally applies to which loss?","choices":["Impact with another vehicle","Theft of the vehicle","Hail damage","Flood damage"],"answer":0,"explanation":"Collision is upset or impact with another object or vehicle."},
    {"id":"q7","module_id":"homeowners","question":"A detached garage is usually associated with which homeowners coverage?","choices":["Coverage A","Coverage B","Coverage C","Coverage D"],"answer":1,"explanation":"Coverage B generally applies to other structures."},
    {"id":"q8","module_id":"commercial","question":"Which CGL coverage part addresses bodily injury and property damage liability?","choices":["Coverage A","Coverage B","Coverage C","Coverage D"],"answer":0,"explanation":"CGL Coverage A is bodily injury and property damage liability."},
    {"id":"q9","module_id":"workers-comp","question":"Workers compensation is generally designed to cover what?","choices":["Work-related injury or disease","Home maintenance","Personal auto damage","Intentional crime by customers"],"answer":0,"explanation":"Workers compensation addresses job-related injury or occupational disease."},
    {"id":"q10","module_id":"ethics","question":"Which conduct involves replacing a policy through misleading information?","choices":["Twisting","Coinsurance","Subrogation","Indemnity"],"answer":0,"explanation":"Twisting generally involves improper replacement through misleading information."}
]

TERM_DEFINITIONS = {
    "risk": "The chance or uncertainty of financial loss.",
    "premium": "The amount paid for insurance coverage.",
    "loss": "Financial damage caused by a covered or potentially covered event.",
    "insurer": "The insurance company that issues the policy.",
    "insured": "The person or organization protected by the policy.",
    "peril": "The cause of loss, such as fire, theft, wind, or collision.",
    "hazard": "A condition that increases the chance or severity of loss.",
    "deductible": "The amount the insured pays before insurance responds to a covered loss.",
    "replacement cost": "The cost to replace damaged property without depreciation, subject to policy terms.",
    "actual cash value": "Replacement cost minus depreciation, subject to policy terms.",
    "negligence": "Failure to use reasonable care, causing harm to another person or property.",
    "occurrence": "An accident or event that may trigger coverage under an occurrence-based policy.",
    "aggregate": "The most a policy will pay for all covered losses during a policy period.",
    "endorsement": "A form that changes the policy by adding, removing, or modifying coverage.",
    "exclusion": "Policy language that removes coverage for certain causes, property, people, or situations."
}


def load_course_data() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    if SEED_PATH.exists():
        with SEED_PATH.open("r", encoding="utf-8") as f:
            data = json.load(f)
        modules = data.get("modules") or FALLBACK_MODULES
        questions = data.get("questions") or FALLBACK_QUESTIONS
        flashcards = data.get("flashcards") or []
        return modules, questions, flashcards
    return FALLBACK_MODULES, FALLBACK_QUESTIONS, []

MODULES, QUESTIONS, SEEDED_FLASHCARDS = load_course_data()

class ProgressIn(BaseModel):
    learner_id: str = Field(default="default", min_length=1, max_length=80)
    lesson_id: str = Field(min_length=1, max_length=120)
    completed: bool = True
    confidence: int = Field(default=0, ge=0, le=3)
    note: str = Field(default="", max_length=5000)
    saved: bool = False

class QuizSubmit(BaseModel):
    learner_id: str = Field(default="default", min_length=1, max_length=80)
    answers: dict[str, int] = Field(default_factory=dict)

class TutorIn(BaseModel):
    message: str = Field(min_length=1, max_length=1200)

@contextmanager
def conn() -> Iterator[sqlite3.Connection]:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    db_conn = sqlite3.connect(DB_PATH)
    db_conn.row_factory = sqlite3.Row
    try:
        yield db_conn
        db_conn.commit()
    except Exception:
        db_conn.rollback()
        raise
    finally:
        db_conn.close()


def init_db() -> None:
    with conn() as c:
        c.executescript("""
        create table if not exists progress (
            learner_id text not null,
            lesson_id text not null,
            completed integer not null default 0,
            confidence integer not null default 0,
            note text not null default '',
            saved integer not null default 0,
            updated_at integer not null,
            primary key (learner_id, lesson_id)
        );
        create table if not exists mistakes (
            id integer primary key autoincrement,
            learner_id text not null,
            question_id text not null,
            selected integer not null,
            correct integer not null,
            created_at integer not null
        );
        """)

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


def configured_origins() -> list[str]:
    raw = os.environ.get("CORS_ORIGINS", "*").strip()
    return [x.strip() for x in raw.split(",") if x.strip()] or ["*"]

app = FastAPI(title="P&C License Prep Academy API", version="1.1.0", lifespan=lifespan)
origins = configured_origins()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False if origins == ["*"] else True,
    allow_methods=["*"],
    allow_headers=["*"],
)
if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")

@app.get("/")
def home():
    index = FRONTEND_DIR / "index.html"
    if index.exists():
        return FileResponse(str(index))
    return {"ok": True, "app": "P&C License Prep Academy API"}

@app.get("/api/health")
def health():
    return {"ok": True, "modules": len(MODULES), "questions": len(QUESTIONS), "seed_file_loaded": SEED_PATH.exists()}

@app.get("/api/modules")
def modules():
    return [{"id": m["id"], "title": m["title"], "lesson_count": len(m.get("lessons", []))} for m in MODULES]

@app.get("/api/modules/{module_id}")
def module_detail(module_id: str):
    module = next((m for m in MODULES if m["id"] == module_id), None)
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    return module

@app.get("/api/lessons/{lesson_id}")
def lesson_detail(lesson_id: str):
    for module in MODULES:
        for lesson in module.get("lessons", []):
            if lesson["id"] == lesson_id:
                return {**lesson, "module_id": module["id"], "module_title": module["title"]}
    raise HTTPException(status_code=404, detail="Lesson not found")

@app.get("/api/progress")
def get_progress(learner_id: str = Query("default", min_length=1, max_length=80)):
    with conn() as c:
        rows = c.execute("select * from progress where learner_id=?", (learner_id,)).fetchall()
        mistake_count = c.execute("select count(*) c from mistakes where learner_id=?", (learner_id,)).fetchone()["c"]
    all_lessons = [l for m in MODULES for l in m.get("lessons", [])]
    completed = sum(1 for r in rows if r["completed"])
    avg_conf = round(sum(r["confidence"] for r in rows) / max(len(rows), 1), 1)
    return {"total_lessons": len(all_lessons), "completed_lessons": completed, "percent_complete": round(completed / max(len(all_lessons), 1) * 100), "average_confidence": avg_conf, "mistake_count": mistake_count, "items": [dict(r) for r in rows]}

@app.post("/api/progress")
def save_progress(payload: ProgressIn):
    now = int(time.time())
    with conn() as c:
        c.execute("insert into progress(learner_id,lesson_id,completed,confidence,note,saved,updated_at) values(?,?,?,?,?,?,?) on conflict(learner_id,lesson_id) do update set completed=excluded.completed, confidence=excluded.confidence, note=excluded.note, saved=excluded.saved, updated_at=excluded.updated_at", (payload.learner_id, payload.lesson_id, int(payload.completed), payload.confidence, payload.note, int(payload.saved), now))
    return {"ok": True}

@app.get("/api/questions")
def question_set(module_id: str | None = None, limit: int = Query(10, ge=1, le=50)):
    qs = [q for q in QUESTIONS if module_id is None or q.get("module_id") == module_id]
    if not qs:
        qs = QUESTIONS[:]
    random.shuffle(qs)
    return [{k: v for k, v in q.items() if k != "answer"} for q in qs[:limit]]

@app.post("/api/questions/submit")
def submit_quiz(payload: QuizSubmit):
    if len(payload.answers) > 50:
        raise HTTPException(status_code=400, detail="Submit 50 answers or fewer at once")
    by_id = {q["id"]: q for q in QUESTIONS}
    results = []
    correct_count = 0
    now = int(time.time())
    with conn() as c:
        for qid, selected in payload.answers.items():
            q = by_id.get(qid)
            if not q:
                continue
            if selected < 0 or selected >= len(q.get("choices", [])):
                raise HTTPException(status_code=400, detail=f"Invalid answer choice for {qid}")
            is_correct = int(selected) == int(q["answer"])
            correct_count += 1 if is_correct else 0
            if not is_correct:
                c.execute("insert into mistakes(learner_id,question_id,selected,correct,created_at) values(?,?,?,?,?)", (payload.learner_id, qid, int(selected), int(q["answer"]), now))
            results.append({"id": qid, "correct": is_correct, "selected": selected, "answer": q["answer"], "explanation": q["explanation"]})
    total = max(len(results), 1)
    return {"score": round(correct_count / total * 100), "correct": correct_count, "total": total, "results": results}

@app.get("/api/mistakes")
def mistakes(learner_id: str = Query("default", min_length=1, max_length=80), limit: int = Query(50, ge=1, le=100)):
    by_id = {q["id"]: q for q in QUESTIONS}
    with conn() as c:
        rows = c.execute("select * from mistakes where learner_id=? order by created_at desc limit ?", (learner_id, limit)).fetchall()
    return [{"id": r["id"], "question": by_id.get(r["question_id"], {}), "selected": r["selected"], "correct": r["correct"], "created_at": r["created_at"]} for r in rows]

@app.get("/api/flashcards")
def flashcards():
    if SEEDED_FLASHCARDS:
        return SEEDED_FLASHCARDS
    cards = []
    seen = set()
    for m in MODULES:
        for lesson in m.get("lessons", []):
            for term in lesson.get("terms", []):
                key = term.lower()
                if key not in seen:
                    seen.add(key)
                    cards.append({"term": term, "definition": TERM_DEFINITIONS.get(key, lesson["body"]), "module": m["title"]})
    return cards

@app.get("/api/study-plan")
def study_plan(learner_id: str = Query("default", min_length=1, max_length=80)):
    progress = get_progress(learner_id)
    completed_ids = {p["lesson_id"] for p in progress["items"] if p["completed"]}
    next_lessons = []
    for m in MODULES:
        for lesson in m.get("lessons", []):
            if lesson["id"] not in completed_ids:
                next_lessons.append({"module_id": m["id"], "module": m["title"], "lesson_id": lesson["id"], "lesson": lesson["title"]})
            if len(next_lessons) >= 5:
                break
        if len(next_lessons) >= 5:
            break
    return {"readiness_score": max(10, min(95, progress["percent_complete"] - min(progress["mistake_count"], 20))), "recommended_lessons": next_lessons, "tip": "Focus on unfinished lessons, then drill mistakes until your scores are consistently above 85%."}

@app.post("/api/tutor")
def tutor(payload: TutorIn):
    text = payload.message.lower()
    matches = []
    for m in MODULES:
        for lesson in m.get("lessons", []):
            haystack = (lesson["title"] + " " + lesson["body"] + " " + " ".join(lesson.get("terms", []))).lower()
            if any(word in haystack for word in text.split() if len(word) > 3):
                matches.append(f"{lesson['title']}: {lesson['body']}")
    if not matches:
        matches = ["Start by identifying whether the question is about property coverage, liability coverage, contract language, or producer conduct."]
    return {"answer": "Coverage Coach: " + " ".join(matches[:2]), "guardrail": "General exam prep only. This endpoint is keyword-matched and is not an AI model."}
