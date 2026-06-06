from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="P&C License Prep Academy V1")

HTML = """
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>P&C License Prep Academy</title>
<style>
:root{--page:#eef1fb;--line:#dfe3eb;--paper:#fff;--ink:#202124;--muted:#6f7377;--blue:#00AEEF;--radius:22px}*{box-sizing:border-box}body{margin:0;height:100vh;overflow:hidden;background:var(--page);font-family:Inter,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;color:var(--ink)}button{border:0;border-radius:999px;padding:.65rem .95rem;font:inherit;font-weight:750;cursor:pointer}.workspace{height:100vh;display:grid;grid-template-columns:minmax(300px,25vw) minmax(520px,1fr) minmax(320px,25vw);gap:12px;padding:0 16px 14px}.pane{background:var(--paper);border:1px solid var(--line);border-radius:0 0 var(--radius) var(--radius);display:flex;flex-direction:column;min-height:0;overflow:hidden}.pane-head{height:60px;display:flex;align-items:center;justify-content:space-between;padding:0 20px;border-bottom:1px solid var(--line)}.pane-head h2{font-size:1.18rem;margin:0}.icon{width:34px;height:34px;border-radius:50%;display:grid;place-items:center;background:#f1f3f7}.pane-body{padding:18px;overflow:auto;flex:1}.add{width:100%;background:#fff;border:1px solid var(--line);font-size:1rem;margin-bottom:20px}.search{border:1px solid var(--line);border-radius:18px;background:#fbfcff;padding:14px;margin-bottom:20px}.search input{width:100%;border:0;outline:0;background:transparent;font-size:1rem}.chips{display:flex;gap:8px;margin-top:16px}.chips button{background:#fff;border:1px solid var(--line);color:#2d3135}.empty{height:55%;display:grid;place-items:center;text-align:center;color:var(--muted);padding:1rem}.empty .big,.spark{font-size:2rem;color:#777}.messages{flex:1;overflow:auto;padding:0 8px 0 0}.intro{font-size:1.05rem;line-height:1.5}.intro strong{font-weight:850}.note-actions{display:flex;gap:12px;align-items:center;margin:18px 0}.note-actions button{background:#fff;border:1px solid var(--line);color:#333}.suggestions{display:flex;flex-direction:column;gap:10px;align-items:flex-start;margin-top:18px}.suggestions button{background:#f7f7f8;color:#303236;border-radius:14px;font-weight:500}.composer{display:flex;align-items:center;gap:10px;border:1px solid #d6deeb;border-radius:18px;background:#fff;padding:12px 14px;margin-top:auto}.composer textarea{min-height:38px;max-height:110px;resize:none;flex:1;border:0;outline:0;padding:0;font-size:1rem}.meta{font-size:.84rem;color:var(--muted);white-space:nowrap}.send{width:48px;height:48px;border-radius:50%;display:grid;place-items:center;font-size:1.4rem;padding:0;background:#e7e9ed;color:#4a4d51}.studio-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px}.tile{min-height:70px;border-radius:14px;display:flex;align-items:center;justify-content:space-between;padding:14px;text-align:left;font-weight:850}.tile-a{background:#e9eefc;color:#163c8c}.tile-b{background:#f3f1df;color:#655610}.tile-c{background:#dff2e4;color:#0d6531}.tile-d{background:#f2e7f0;color:#873175}.tile-e{background:#f1f1e4;color:#6b5c17}.tile-f{background:#f7e9e9;color:#9d2828}.tile-g{background:#def3f9;color:#00739c}.tile-h{background:#f0e7f0;color:#7d317d}.tile-i{background:#e9eefc;color:#173d88}.studio-output{margin-top:18px;border-top:1px solid var(--line);padding-top:18px;min-height:220px;display:grid;place-items:center;text-align:center;color:#3b3e42}.primary{background:#000;color:white}@media(max-width:1100px){body{overflow:auto}.workspace{height:auto;min-height:100vh;grid-template-columns:1fr}.pane{border-radius:20px}}
</style>
</head>
<body>
<div class="workspace">
  <aside class="pane">
    <div class="pane-head"><h2>Sources</h2><div class="icon">▣</div></div>
    <div class="pane-body">
      <button class="add">＋ Add sources</button>
      <div class="search"><input placeholder="Search the web for new sources"><div class="chips"><button>🌐 Web⌄</button><button>✦ Fast Research⌄</button><button class="icon">⌕</button></div></div>
      <div class="empty"><div><div class="big">▧</div><strong>Saved sources will appear here</strong><p>Click Add source above to add PDFs, websites, text, videos, or audio files. Or import a file directly from Google Drive.</p></div></div>
    </div>
  </aside>
  <section class="pane">
    <div class="pane-head"><h2>Chat</h2><div class="icon">⋮</div></div>
    <div class="pane-body" style="display:flex;flex-direction:column;gap:16px">
      <div class="messages"><div class="intro"><p>Welcome to <strong>P&C License Prep Academy</strong>.</p><p>This restored V1 service is only a visual fallback. The full working product is in <strong>pc-license-prep-server-v2</strong>.</p><p>For the real app, deploy V2 with Root Directory set to <strong>pc-license-prep-server-v2</strong>.</p><div class="note-actions"><button>⚑ Save to note</button><button class="icon">▥</button><button class="icon">👍</button><button class="icon">👎</button></div></div></div>
      <div class="suggestions"><button>I have a mix of PDFs and text files</button><button>Can you explain how to add website links instead?</button><button>How many files can I upload to one notebook?</button></div>
      <div class="composer"><textarea placeholder="Ask a question or create something"></textarea><span class="meta">0 sources</span><button class="send">➜</button></div>
    </div>
  </section>
  <aside class="pane">
    <div class="pane-head"><h2>Studio</h2><div class="icon">▣</div></div>
    <div class="pane-body">
      <div class="studio-grid"><button class="tile tile-a">Audio Overview <b>›</b></button><button class="tile tile-b">Slide Deck <b>›</b></button><button class="tile tile-c">Video Overview <b>›</b></button><button class="tile tile-d">Mind Map <b>›</b></button><button class="tile tile-e">Reports <b>›</b></button><button class="tile tile-f">Flashcards <b>›</b></button><button class="tile tile-g">Quiz <b>›</b></button><button class="tile tile-h">Infographic <b>›</b></button><button class="tile tile-i">Data Table <b>›</b></button></div>
      <div class="studio-output"><div><div class="spark">✦</div><strong>Studio output will be saved here.</strong><p>After adding sources, click to add Audio Overview, Study Guide, Mind Map, and more!</p><button class="primary">Add note</button></div></div>
    </div>
  </aside>
</div>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def home():
    return HTML

@app.get("/api/health")
def health():
    return {"ok": True, "version": "v1-visual-fallback", "note": "Deploy pc-license-prep-server-v2 for the full app."}
