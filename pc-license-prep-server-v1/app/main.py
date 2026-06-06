from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="P&C License Prep Academy V1")

MODULES = [
    {"id": "basics", "title": "Insurance Basics", "lessons": [
        {"id": "what-is-insurance", "title": "What Is Insurance?", "body": "Insurance transfers financial risk from the insured to the insurer. The insured pays premium and the insurer pays covered losses according to the policy."},
        {"id": "risk-peril-hazard", "title": "Risk, Peril, and Hazard", "body": "Risk is the chance of loss. A peril is the cause of loss. A hazard is something that increases the chance or severity of loss."}
    ]},
    {"id": "contracts", "title": "Insurance Contracts", "lessons": [
        {"id": "policy-parts", "title": "Policy Parts", "body": "Policies usually include declarations, insuring agreement, conditions, exclusions, and endorsements."}
    ]},
    {"id": "property", "title": "Property Fundamentals", "lessons": [
        {"id": "acv-rc", "title": "ACV and Replacement Cost", "body": "Actual cash value is commonly replacement cost minus depreciation. Replacement cost pays to replace with like kind and quality, subject to policy terms."}
    ]},
    {"id": "casualty", "title": "Casualty Fundamentals", "lessons": [
        {"id": "liability", "title": "Liability Basics", "body": "Liability coverage is third-party coverage for bodily injury or property damage claims made by others against the insured."}
    ]}
]

QUESTIONS = [
    {"id": "q1", "module_id": "basics", "question": "What is a peril?", "choices": ["The cause of loss", "The premium", "The insured", "The limit"], "answer": 0, "explanation": "A peril is the cause of loss."},
    {"id": "q2", "module_id": "basics", "question": "Faulty wiring is best described as what?", "choices": ["A policy limit", "A hazard", "A deductible", "A declaration"], "answer": 1, "explanation": "Faulty wiring is a physical hazard."},
    {"id": "q3", "module_id": "contracts", "question": "Which policy section summarizes the insured, limits, and policy dates?", "choices": ["Declarations", "Exclusions", "Subrogation", "Coinsurance"], "answer": 0, "explanation": "The declarations page is the policy snapshot."},
    {"id": "q4", "module_id": "property", "question": "Actual cash value is commonly replacement cost minus what?", "choices": ["Premium", "Depreciation", "Policy number", "Insurable interest"], "answer": 1, "explanation": "ACV commonly subtracts depreciation."}
]

HTML = """
<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'><title>P&C License Prep V1</title><style>body{font-family:system-ui;margin:0;background:#f6fbff;color:#081521}.top{padding:18px 24px;background:#fff;border-bottom:1px solid #d8e8ef}.wrap{max-width:1100px;margin:24px auto;padding:0 18px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px}.card{background:#fff;border:1px solid #d8e8ef;border-radius:22px;padding:18px;box-shadow:0 10px 30px #0001}button{border:0;border-radius:999px;padding:10px 14px;background:#00AEEF;color:white;font-weight:800}.muted{color:#667085}</style></head><body><div class='top'><strong>P&C License Prep Academy</strong><div class='muted'>V1 restored starter</div></div><main class='wrap'><section class='card'><h1>Study smarter. Pass with confidence.</h1><p>General Property and Casualty licensing prep starter.</p><button onclick='loadModules()'>Load Modules</button> <button onclick='loadQuiz()'>Practice Quiz</button></section><div id='out' class='grid' style='margin-top:16px'></div></main><script>async function j(u,o){return fetch(u,o).then(r=>r.json())}async function loadModules(){let m=await j('/api/modules');out.innerHTML=m.map(x=>`<div class='card'><h2>${x.title}</h2><p>${x.lesson_count} lessons</p><button onclick="openModule('${x.id}')">Open</button></div>`).join('')}async function openModule(id){let m=await j('/api/modules/'+id);out.innerHTML=m.lessons.map(l=>`<div class='card'><h2>${l.title}</h2><p>${l.body}</p></div>`).join('')}async function loadQuiz(){let qs=await j('/api/questions');out.innerHTML=qs.map((q,i)=>`<div class='card'><h3>${q.question}</h3>${q.choices.map((c,n)=>`<p><button onclick='alert(${JSON.stringify(q.explanation)})'>${c}</button></p>`).join('')}</div>`).join('')}</script></body></html>
"""

@app.get("/", response_class=HTMLResponse)
def home():
    return HTML

@app.get("/api/health")
def health():
    return {"ok": True, "version": "v1-restored", "modules": len(MODULES), "questions": len(QUESTIONS)}

@app.get("/api/modules")
def modules():
    return [{"id": m["id"], "title": m["title"], "lesson_count": len(m["lessons"])} for m in MODULES]

@app.get("/api/modules/{module_id}")
def module_detail(module_id: str):
    for m in MODULES:
        if m["id"] == module_id:
            return m
    return {"error": "not found"}

@app.get("/api/questions")
def questions(module_id: str | None = None):
    return [{k: v for k, v in q.items() if k != "answer"} for q in QUESTIONS if module_id is None or q["module_id"] == module_id]

@app.post("/api/questions/submit")
def submit(payload: dict):
    answers = payload.get("answers", {})
    by_id = {q["id"]: q for q in QUESTIONS}
    correct = 0
    results = []
    for qid, selected in answers.items():
        q = by_id.get(qid)
        if not q:
            continue
        ok = int(selected) == q["answer"]
        correct += 1 if ok else 0
        results.append({"id": qid, "correct": ok, "answer": q["answer"], "explanation": q["explanation"]})
    total = max(len(results), 1)
    return {"score": round(correct / total * 100), "results": results}
