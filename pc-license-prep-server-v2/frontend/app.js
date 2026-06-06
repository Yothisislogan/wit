const app=document.getElementById('app');
const toastEl=document.getElementById('toast');
let me=null;let modules=[];let currentQuestions=[];let answers={};let chatMessages=[];
function toast(msg){toastEl.textContent=msg;toastEl.classList.add('show');setTimeout(()=>toastEl.classList.remove('show'),2200)}
async function api(path,opts={}){const res=await fetch(path,{headers:{'Content-Type':'application/json'},...opts});if(!res.ok){throw new Error(await res.text())}return res.json()}
function esc(s=''){return String(s).replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[m]))}
async function boot(){const m=await api('/api/me');me=m.user;if(!me){return loginScreen()}modules=await api('/api/modules');chatMessages=[];route('dashboard')}
async function loginScreen(){const p=await api('/auth/providers');app.innerHTML=`<section class="login card"><div class="eyebrow">Free public access</div><h1>Sign in to save your progress</h1><p class="muted">Use Google, Microsoft, or Facebook. Local development can use the demo login.</p>${p.providers.map(x=>`<a class="provider" href="/auth/login/${x.id}"><button class="primary provider" ${x.configured?'':'disabled'}>Continue with ${esc(x.name)}${x.configured?'':' — not configured'}</button></a>`).join('')}${p.dev_login_enabled?'<a class="provider" href="/auth/dev-login"><button class="ghost provider">Development Login</button></a>':''}</section>`}
async function route(name,arg){try{if(!me)return loginScreen();if(name==='dashboard')return showDashboard();if(name==='modules')return showModules();if(name==='module')return showModule(arg);if(name==='lesson')return showLesson(arg);if(name==='terms')return terms();if(name==='quiz')return quiz(arg);if(name==='coach')return workspace()}catch(e){app.innerHTML=`<div class="page-wrap"><div class="card"><h2>Something went wrong</h2><p>${esc(e.message)}</p></div></div>`}}
function sourcePanel(){return `<aside class="pane"><div class="pane-head"><h2>Sources</h2><div class="pane-tools"><button class="icon-btn">▣</button></div></div><div class="pane-body"><button class="ghost" style="width:100%;font-size:1rem;margin-bottom:20px" onclick="route('modules')">＋ Add sources</button><div class="source-search"><input placeholder="Search the web for new sources"><div class="source-actions"><button>🌐 Web⌄</button><button>✦ Fast Research⌄</button><button class="icon-btn" style="margin-left:auto">⌕</button></div></div><div class="empty-state"><div><div class="big">▧</div><strong>Saved sources will appear here</strong><p>Click Add source above to add PDFs, websites, text, videos, or audio files. Or import a file directly from Google Drive.</p></div></div></div></aside>`}
function chatPanel(){const defaultIntro=`<div class="message assistant intro"><p>Once unzipped, you can upload the individual files—like <strong>PDFs, Google Docs, or even text files</strong>—using the <strong>Source Panel</strong> on the left. You can also add website links or YouTube URLs if those are part of your project!</p><p>By uploading these sources, I can help you summarize the contents, find specific details, or even generate a <strong>Study Guide</strong> or <strong>Audio Overview</strong> to help you process everything quickly.</p><p>What kind of files do you have inside that ZIP folder? I'd be happy to help you figure out the best way to bring them in!</p><div class="note-actions"><button class="ghost">⚑ Save to note</button><button class="icon-btn">▥</button><button class="icon-btn">👍</button><button class="icon-btn">👎</button></div></div>`;return `<section class="pane center"><div class="pane-head"><h2>Chat</h2><div class="pane-tools"><button class="icon-btn">⋮</button></div></div><div class="pane-body chat-body"><div class="messages" id="messages">${defaultIntro}${chatMessages.map(m=>`<div class="message ${m.role}">${esc(m.text)}</div>`).join('')}</div><div class="suggestions"><button onclick="quickAsk('I have a mix of PDFs and text files')">I have a mix of PDFs and text files</button><button onclick="quickAsk('Can you explain how to add website links instead?')">Can you explain how to add website links instead?</button><button onclick="quickAsk('How many files can I upload to one notebook?')">How many files can I upload to one notebook?</button></div><div class="composer"><textarea id="coachQuestion" placeholder="Ask a question or create something"></textarea><span class="composer-meta">0 sources</span><button class="send-btn" onclick="askCoach()">➜</button></div></div></section>`}
function studioPanel(){return `<aside class="pane"><div class="pane-head"><h2>Studio</h2><div class="pane-tools"><button class="icon-btn">▣</button></div></div><div class="pane-body"><div class="studio-grid"><button class="studio-tile tile-audio" onclick="studio('audio')"><span>▥<br>Audio Overview</span><b>›</b></button><button class="studio-tile tile-deck" onclick="studio('deck')"><span>▤<br>Slide Deck</span><b>›</b></button><button class="studio-tile tile-video" onclick="studio('video')"><span>▣<br>Video Overview</span><b>›</b></button><button class="studio-tile tile-map" onclick="studio('map')"><span>⌘<br>Mind Map</span><b>›</b></button><button class="studio-tile tile-report" onclick="studio('report')"><span>⇱<br>Reports</span><b>›</b></button><button class="studio-tile tile-flash" onclick="route('terms')"><span>▧<br>Flashcards</span><b>›</b></button><button class="studio-tile tile-quiz" onclick="route('quiz')"><span>▢<br>Quiz</span><b>›</b></button><button class="studio-tile tile-info" onclick="studio('infographic')"><span>▥<br>Infographic</span><b>›</b></button><button class="studio-tile tile-data" onclick="studio('data')"><span>▦<br>Data Table</span><b>›</b></button></div><div class="studio-output" id="studioOutput"><div><div class="spark">✦</div><strong>Studio output will be saved here.</strong><p>After adding sources, click to add Audio Overview, Study Guide, Mind Map, and more!</p><button class="primary" onclick="quickAsk('Create a study guide for the Property and Casualty licensing course.')">▣ Add note</button></div></div></div></aside>`}
async function workspace(){app.innerHTML=`<div class="workspace"><div class="ws-topbar"><button class="ws-back-btn" onclick="showDashboard()">← Dashboard</button><span class="ws-topbar-title">◈ Study Workspace</span></div><div class="ws-panels">${sourcePanel()}${chatPanel()}${studioPanel()}</div></div>`;scrollMessages();if(typeof studioModuleSlug!=='undefined'&&!studioModuleSlug&&modules.length){studioModuleSlug=modules[0].slug;const sel=document.getElementById('studioModuleSelect');if(sel)sel.value=studioModuleSlug;}}
function scrollMessages(){setTimeout(()=>{const el=document.getElementById('messages');if(el)el.scrollTop=el.scrollHeight},50)}
function quickAsk(text){const q=document.getElementById('coachQuestion');if(q){q.value=text;askCoach()}else{chatMessages.push({role:'user',text});route('dashboard').then(()=>askCoachText(text))}}
async function askCoach(){const box=document.getElementById('coachQuestion');const message=(box?.value||'').trim();if(!message){toast('Ask a question first');return}box.value='';await askCoachText(message)}
async function askCoachText(message){chatMessages.push({role:'user',text:message});await workspace();chatMessages.push({role:'assistant',text:'Coverage Coach is thinking...'});await workspace();const out=await api('/api/tutor/ask',{method:'POST',body:JSON.stringify({message})});chatMessages.pop();chatMessages.push({role:'assistant',text:out.answer});await workspace();toast((out.mode||'coach')==='openai'?'Answered with Coverage Coach':'Answered in fallback mode')}
async function studio(kind){const out=document.getElementById('studioOutput');if(!out)return;const content={audio:'Create an audio-style summary of the next best topic I should study.',deck:'Create a slide deck outline for the core P&C modules.',video:'Create a short video overview script for general P&C licensing prep.',map:'Create a mind map of the P&C course modules.',report:'Summarize my study progress and weak areas.',infographic:'Create an infographic outline for risk, peril, hazard, and insurance contracts.',data:'Create a table of modules, lessons, and study priority.'}[kind]||'Create a study output.';out.innerHTML=`<div><div class="spark">✦</div><strong>${esc(kind.toUpperCase())}</strong><p>${esc(content)}</p><button class="primary" onclick="quickAsk('${esc(content)}')">Generate in Chat</button></div>`}
async function showModules(){app.innerHTML=`<div class="page-wrap"><div class="card"><button onclick="route('dashboard')">← Workspace</button><h1>Course Sources</h1><p class="muted">These are your built-in P&C study sources.</p><div class="grid">${modules.map(m=>`<div class="card"><div class="eyebrow">${m.lesson_count} lessons</div><h2>${esc(m.title)}</h2><p class="muted">${esc(m.description)}</p><button onclick="route('module','${m.slug}')">Open</button></div>`).join('')}</div></div></div>`}
async function showModule(slug){const m=await api('/api/modules/'+slug);app.innerHTML=`<div class="page-wrap"><div class="card"><button onclick="route('dashboard')">← Workspace</button><h1>${esc(m.title)}</h1><p class="muted">${esc(m.description)}</p><div class="list">${m.lessons.map(l=>`<div class="row"><div><strong>${esc(l.title)}</strong><br><span class="muted">${esc(l.summary)}</span></div><button onclick="route('lesson','${l.slug}')">Study</button></div>`).join('')}</div><div class="toolbar"><button onclick="route('quiz','${m.slug}')">Quiz This Module</button><button onclick="quickAsk('Explain the ${esc(m.title)} module and quiz me on it.')">Ask Coverage Coach</button></div></div></div>`}
async function showLesson(slug){const l=await api('/api/lessons/'+slug);app.innerHTML=`<div class="page-wrap"><article class="lesson card"><button onclick="route('dashboard')">← Workspace</button><h1>${esc(l.title)}</h1><p class="muted">${esc(l.summary)}</p><p>${esc(l.body)}</p>${l.example?`<h3>Example</h3><p>${esc(l.example)}</p>`:''}${l.memory_tip?`<h3>Memory tip</h3><p>${esc(l.memory_tip)}</p>`:''}<h3>Key terms</h3><p>${l.terms.map(t=>`<span class="term" title="${esc(t.plain_english_definition)}">${esc(t.term)}</span>`).join('')||'<span class="muted">No terms yet.</span>'}</p><label>Confidence</label><select id="confidence"><option value="1">Need review</option><option value="2">Getting it</option><option value="3">Strong</option></select><label>Notes</label><textarea id="notes" placeholder="Study notes..."></textarea><div class="toolbar"><button class="primary" onclick="saveProgress(${l.id})">Mark Complete</button><button onclick="speak('${esc((l.audio_script||l.body).replace(/`/g,''))}')">Listen</button><button onclick="quickAsk('Explain the lesson ${esc(l.title)} and give me one practice question.')">Ask Coverage Coach</button></div></article></div>`}
async function saveProgress(id){await api('/api/lessons/'+id+'/progress',{method:'POST',body:JSON.stringify({completed:true,confidence:Number(document.getElementById('confidence').value),notes:document.getElementById('notes').value,saved_for_review:false})});toast('Progress saved')}
function speak(text){speechSynthesis.cancel();speechSynthesis.speak(new SpeechSynthesisUtterance(text))}
async function terms(){const rows=await api('/api/terms');app.innerHTML=`<div class="page-wrap"><div class="card"><button onclick="route('dashboard')">← Workspace</button><h1>Flashcards</h1><div class="list">${rows.map(t=>`<div class="card"><span class="pill">${esc(t.term)}</span><p><strong>Plain English:</strong> ${esc(t.plain_english_definition)}</p><p><strong>Exam:</strong> ${esc(t.exam_definition)}</p>${t.example?`<p class="muted"><strong>Example:</strong> ${esc(t.example)}</p>`:''}</div>`).join('')}</div></div></div>`}
async function quiz(moduleSlug){answers={};currentQuestions=await api('/api/questions?limit=10'+(moduleSlug?'&module_slug='+encodeURIComponent(moduleSlug):''));renderQuiz()}
function renderQuiz(results=null){app.innerHTML=`<div class="page-wrap"><div class="card"><button onclick="route('dashboard')">← Workspace</button><h1>Quiz</h1>${currentQuestions.map((q,i)=>`<div class="card"><div class="eyebrow">Question ${i+1}</div><h3>${esc(q.question_text)}</h3><div class="choices">${q.choices.map(c=>{let cls='choice';const r=results&&results.find(x=>x.question.id===q.id);if(answers[q.id]===c.id)cls+=' selected';if(r&&c.is_correct)cls+=' correct';if(r&&answers[q.id]===c.id&&!r.is_correct)cls+=' wrong';return `<div class="${cls}" onclick="answers[${q.id}]=${c.id};renderQuiz(${results?'lastResults':'null'})">${esc(c.choice_text)}</div>`}).join('')}</div>${results?`<p>${esc((results.find(x=>x.question.id===q.id)||{}).question?.explanation||'')}</p>`:''}</div>`).join('')}<div class="toolbar"><button class="primary" onclick="submitQuiz()">Submit</button><button onclick="quiz()">New Quiz</button></div></div></div>`}
let lastResults=null;
async function submitQuiz(){const out=await api('/api/quiz/submit',{method:'POST',body:JSON.stringify({mode:'practice',answers})});lastResults=out.results;renderQuiz(lastResults);toast('Score: '+out.score+'%')}
async function logout(){await api('/auth/logout',{method:'POST'});location.reload()}
boot();
async function showDashboard(){
  app.innerHTML='<div class="page-wrap"><p style="padding:2rem;text-align:center;color:var(--text-muted)">Loading your dashboard\u2026</p></div>';
  let d;
  try{d=await api('/api/dashboard');}
  catch(e){
    app.innerHTML='<div class="page-wrap"><div class="card"><h2>Dashboard</h2><p>Could not load progress data.</p><button class="primary" onclick="workspace()">Open Workspace \u2192</button></div></div>';
    return;
  }
  const {readiness,lessons,quizzes,mistakes,modules:mods,recommendations:recs,user:uname}=d;
  const ringColor=readiness>=80?'#10b981':readiness>=60?'#f59e0b':'#ef4444';
  const ringLabel=readiness>=80?'\u2713 Exam Ready':readiness>=60?'\u2191 Getting There':'\u26a1 Keep Studying';
  const circ=(2*Math.PI*40);
  const dash=(circ*readiness/100).toFixed(1);
  const ring=`<svg class="dash-ring-svg" viewBox="0 0 100 100">
    <circle cx="50" cy="50" r="40" fill="none" stroke="var(--border)" stroke-width="10"/>
    <circle cx="50" cy="50" r="40" fill="none" stroke="${ringColor}" stroke-width="10"
      stroke-dasharray="${dash} ${circ.toFixed(1)}" stroke-linecap="round"
      transform="rotate(-90 50 50)" style="transition:stroke-dasharray .6s"/>
    <text x="50" y="46" text-anchor="middle" font-size="20" font-weight="700" fill="${ringColor}">${readiness}%</text>
    <text x="50" y="62" text-anchor="middle" font-size="7" fill="var(--text-muted)">Readiness</text>
  </svg>`;
  const bars=quizzes.recent.length
    ?quizzes.recent.slice().reverse().map(q=>{
        const h=Math.max(8,Math.round(q.score*.65)),c=q.score>=80?'#10b981':q.score>=60?'#f59e0b':'#ef4444';
        return `<div class="dash-bar-wrap" title="${q.score}%"><div class="dash-bar" style="height:${h}px;background:${c}"></div><span class="dash-bar-lbl">${q.score}</span></div>`;
      }).join('')
    :'<p class="dash-empty-sm">No quizzes yet</p>';
  const modCards=mods.map(m=>{
    const dc=m.pct===100?'#10b981':m.pct>0?'#6366f1':'var(--text-muted)';
    return `<button class="dash-mod-card" onclick="route('module','${esc(m.slug)}')">
      <div class="dash-mod-hdr"><span class="dash-mod-name">${esc(m.title)}</span><span class="dash-mod-pct" style="color:${dc}">${m.pct}%</span></div>
      <div class="dash-progbar"><div class="dash-progfill${m.pct===100?' dash-progfull':''}" style="width:${Math.max(m.pct,2)}%"></div></div>
      <div class="dash-mod-meta">${m.completed_lessons} / ${m.total_lessons} lessons</div>
    </button>`;
  }).join('');
  const mistakeItems=mistakes.top.length
    ?mistakes.top.map(m=>`<li class="dash-mistake-item"><span class="dash-miss-badge">${m.times_missed}\xd7</span><span class="dash-miss-q">${esc(m.question)}</span></li>`).join('')
    :'<li class="dash-no-data">No mistakes yet \u2014 great start!</li>';
  const recCards=(recs||[]).slice(0,4).map(r=>
    `<button class="dash-rec-card" onclick="route('lesson','${esc(r.lesson_slug)}')">
      <div class="dash-rec-mod">${esc(r.module_title)}</div>
      <div class="dash-rec-title">${esc(r.lesson_title)}</div>
      <div class="dash-rec-eta">\u223c${r.estimated_minutes} min \u2192</div>
    </button>`
  ).join('');

  app.innerHTML=`
  <div class="dash-page">
    <header class="dash-topbar-home">
      <span class="dash-brand">\u25c8 P&amp;C Prep Academy</span>
      <button class="primary dash-ws-btn" onclick="workspace()">Workspace \u2192</button>
    </header>
    <div class="dash-wrap">
      <h1 class="dash-welcome">Welcome back${uname?', <strong>'+esc(uname)+'</strong>':''}!</h1>
      <div class="dash-hero">
        <div class="dash-hero-ring">${ring}<div class="dash-ring-label" style="color:${ringColor}">${ringLabel}</div></div>
        <div class="dash-hero-stats">
          <div class="dash-stat-card"><div class="dash-stat-num">${lessons.completed}</div><div class="dash-stat-lbl">Lessons<br>Complete</div></div>
          <div class="dash-stat-card"><div class="dash-stat-num">${lessons.total}</div><div class="dash-stat-lbl">Total<br>Lessons</div></div>
          <div class="dash-stat-card"><div class="dash-stat-num">${quizzes.total_taken}</div><div class="dash-stat-lbl">Quizzes<br>Taken</div></div>
          <div class="dash-stat-card${quizzes.avg_score>=80?' stat-pass':quizzes.avg_score>=60?' stat-warn':''}">
            <div class="dash-stat-num">${quizzes.avg_score||'\u2014'}%</div><div class="dash-stat-lbl">Quiz<br>Average</div></div>
        </div>
        ${quizzes.recent.length?`<div class="dash-quiz-chart"><div class="dash-chart-lbl">Recent Scores</div><div class="dash-bars">${bars}</div></div>`:''}
      </div>
      <section class="dash-section">
        <h2 class="dash-section-title">Module Progress</h2>
        <div class="dash-mod-grid">${modCards||'<p class="dash-empty">No modules loaded yet.</p>'}</div>
      </section>
      <div class="dash-bottom">
        <section class="dash-card dash-half">
          <h2 class="dash-section-title">Mistake Bank <span class="dash-pill">${mistakes.count}</span></h2>
          <ul class="dash-mistake-list">${mistakeItems}</ul>
          ${mistakes.count>5?'<button class="ghost" onclick="route(\'quiz\')">Practice all mistakes \u2192</button>':''}
        </section>
        ${recCards?`<section class="dash-card dash-half">
          <h2 class="dash-section-title">Up Next</h2>
          <div class="dash-recs">${recCards}</div>
        </section>`:''}
      </div>
    </div>
  </div>`;
}
