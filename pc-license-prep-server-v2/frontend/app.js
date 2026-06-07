const app=document.getElementById('app');
const toastEl=document.getElementById('toast');
let me=null;let modules=[];let currentQuestions=[];let answers={};let chatMessages=[];let studioModuleSlug='';
function toast(msg){toastEl.textContent=msg;toastEl.classList.add('show');setTimeout(()=>toastEl.classList.remove('show'),2200)}
async function api(path,opts={}){const res=await fetch(path,{headers:{'Content-Type':'application/json'},...opts});if(!res.ok){throw new Error(await res.text())}return res.json()}
function esc(s=''){return String(s).replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[m]))}
async function boot(){const m=await api('/api/me');me=m.user;if(!me){return loginScreen()}modules=await api('/api/modules');chatMessages=[];route('dashboard')}
async function loginScreen(){const p=await api('/auth/providers');app.innerHTML=`<section class="login card"><div class="eyebrow">Free public access</div><h1>Sign in to save your progress</h1><p class="muted">Use Google, Microsoft, or Facebook. Local development can use the demo login.</p>${p.providers.map(x=>`<a class="provider" href="/auth/login/${x.id}"><button class="primary provider" ${x.configured?'':'disabled'}>Continue with ${esc(x.name)}${x.configured?'':' — not configured'}</button></a>`).join('')}${p.dev_login_enabled?'<a class="provider" href="/auth/dev-login"><button class="ghost provider">Development Login</button></a>':''}</section>`}
async function route(name,arg){try{if(!me)return loginScreen();if(name==='dashboard')return showDashboard();if(name==='modules')return showModules();if(name==='module')return showModule(arg);if(name==='lesson')return showLesson(arg);if(name==='terms')return terms();if(name==='quiz')return quiz(arg);if(name==='coach')return workspace()}catch(e){app.innerHTML=`<div class="page-wrap"><div class="card"><h2>Something went wrong</h2><p>${esc(e.message)}</p></div></div>`}}
function sourcePanel(){return `<aside class="pane"><div class="pane-head"><h2>Sources</h2><div class="pane-tools"><button class="icon-btn">▣</button></div></div><div class="pane-body"><button class="ghost" style="width:100%;font-size:1rem;margin-bottom:20px" onclick="route('modules')">＋ Add sources</button><div class="source-search"><input placeholder="Search the web for new sources"><div class="source-actions"><button>🌐 Web⌄</button><button>✦ Fast Research⌄</button><button class="icon-btn" style="margin-left:auto">⌕</button></div></div><div class="empty-state"><div><div class="big">▧</div><strong>Saved sources will appear here</strong><p>Click Add source above to add PDFs, websites, text, videos, or audio files. Or import a file directly from Google Drive.</p></div></div></div></aside>`}
function chatPanel(){const defaultIntro=`<div class="message assistant intro"><p>Once unzipped, you can upload the individual files—like <strong>PDFs, Google Docs, or even text files</strong>—using the <strong>Source Panel</strong> on the left. You can also add website links or YouTube URLs if those are part of your project!</p><p>By uploading these sources, I can help you summarize the contents, find specific details, or even generate a <strong>Study Guide</strong> or <strong>Practice Quiz</strong> to help you process everything quickly.</p><p>What kind of files do you have inside that ZIP folder? I'd be happy to help you figure out the best way to bring them in!</p><div class="note-actions"><button class="ghost">⚑ Save to note</button><button class="icon-btn">▥</button><button class="icon-btn">👍</button><button class="icon-btn">👎</button></div></div>`;return `<section class="pane center"><div class="pane-head"><h2>Chat</h2><div class="pane-tools"><button class="icon-btn">⋮</button></div></div><div class="pane-body chat-body"><div class="messages" id="messages">${defaultIntro}${chatMessages.map(m=>`<div class="message ${m.role}">${esc(m.text)}</div>`).join('')}</div><div class="suggestions"><button onclick="quickAsk('I have a mix of PDFs and text files')">I have a mix of PDFs and text files</button><button onclick="quickAsk('Can you explain how to add website links instead?')">Can you explain how to add website links instead?</button><button onclick="quickAsk('How many files can I upload to one notebook?')">How many files can I upload to one notebook?</button></div><div class="composer"><textarea id="coachQuestion" placeholder="Ask a question or create something"></textarea><span class="composer-meta">0 sources</span><button class="send-btn" onclick="askCoach()">➜</button></div></div></section>`}
function studioPanel(){
  const opts=modules.map(m=>`<option value="${esc(m.slug)}"${m.slug===studioModuleSlug?' selected':''}>${esc(m.title)}</option>`).join('');
  return `<aside class="pane"><div class="pane-head"><h2>Studio</h2>
  <select id="studioModuleSelect" class="studio-module-select" onchange="studioModuleSlug=this.value">
    <option value="">— pick a module —</option>${opts}
  </select></div>
  <div class="pane-body">
  <div class="studio-grid">
    <button class="studio-tile tile-guide" onclick="studio('study_guide')"><span>◈<br>Study Guide</span><b>›</b></button>
    <button class="studio-tile tile-quiz"  onclick="studio('practice_quiz')"><span>✎<br>Practice Quiz</span><b>›</b></button>
    <button class="studio-tile tile-cram"  onclick="studio('cram_sheet')"><span>⚡<br>Cram Sheet</span><b>›</b></button>
    <button class="studio-tile tile-map"   onclick="studio('concept_map')"><span>⌘<br>Concept Map</span><b>›</b></button>
    <button class="studio-tile tile-flash" onclick="route('terms')"><span>▧<br>Flashcards</span><b>›</b></button>
    <button class="studio-tile tile-exam"  onclick="route('quiz',studioModuleSlug||undefined)"><span>▢<br>Exam Sim</span><b>›</b></button>
  </div>
  <div class="studio-output" id="studioOutput">
    <div class="studio-empty"><div class="spark">✦</div>
    <strong>Pick a module and a tile to generate study content.</strong>
    <p>Study Guide and Practice Quiz use Coverage Coach (Ollama). Cram Sheet is instant.</p></div>
  </div></div></aside>`}
async function workspace(){app.innerHTML=`<div class="workspace"><div class="ws-topbar"><button class="ws-back-btn" onclick="showDashboard()">← Dashboard</button><span class="ws-topbar-title">◈ Study Workspace</span></div><div class="ws-panels">${sourcePanel()}${chatPanel()}${studioPanel()}</div></div>`;scrollMessages();if(typeof studioModuleSlug!=='undefined'&&!studioModuleSlug&&modules.length){studioModuleSlug=modules[0].slug;const sel=document.getElementById('studioModuleSelect');if(sel)sel.value=studioModuleSlug;}}
function scrollMessages(){setTimeout(()=>{const el=document.getElementById('messages');if(el)el.scrollTop=el.scrollHeight},50)}
async function quickAsk(text){
  const q=document.getElementById('coachQuestion');
  if(q){ q.value=text; return askCoach(); }
  // Not on a page with the chat box — go to the workspace first, then ask.
  await workspace();
  const q2=document.getElementById('coachQuestion');
  if(q2){ q2.value=text; return askCoach(); }
  // Last resort: send directly
  return askCoachText(text);
}
async function askCoach(){const box=document.getElementById('coachQuestion');const message=(box?.value||'').trim();if(!message){toast('Ask a question first');return}box.value='';await askCoachText(message)}
async function askCoachText(message){chatMessages.push({role:'user',text:message});await workspace();chatMessages.push({role:'assistant',text:'Coverage Coach is thinking...'});await workspace();const out=await api('/api/tutor/ask',{method:'POST',body:JSON.stringify({message})});chatMessages.pop();chatMessages.push({role:'assistant',text:out.answer});await workspace();toast((out.mode||'coach')==='openai'?'Answered with Coverage Coach':'Answered in fallback mode')}
function studio(action){
  const out=document.getElementById('studioOutput');
  if(!out)return;
  if(!studioModuleSlug){
    out.innerHTML='<div class="studio-msg studio-warn">⚠ Pick a module from the dropdown above first.</div>';
    return;
  }
  const TITLES={study_guide:'Generating Study Guide…',practice_quiz:'Generating Practice Quiz…',cram_sheet:'Loading Cram Sheet…',concept_map:'Generating Concept Map…'};
  out.innerHTML=`<div class="studio-loading"><div class="studio-spinner"></div><p>${TITLES[action]||'Working…'}</p><small>Coverage Coach is thinking — may take 30–60s.</small></div>`;
  api('/api/studio/generate',{method:'POST',body:JSON.stringify({action,module_slug:studioModuleSlug})})
    .then(data=>{
      if(action==='study_guide')        renderStudyGuide(out,data);
      else if(action==='practice_quiz') renderPracticeQuiz(out,data);
      else if(action==='cram_sheet')    renderCramSheet(out,data);
      else if(action==='concept_map')   renderConceptMap(out,data);
      else out.innerHTML=`<pre>${esc(JSON.stringify(data,null,2))}</pre>`;
    })
    .catch(err=>{ out.innerHTML=`<div class="studio-msg studio-error">Error: ${esc(String(err))}</div>`; });
}

function _mdToHtml(text){
  if(!text)return '';
  return text
    .replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')
    .replace(/^## (.+)$/gm,'<h3 class="studio-h3">$1</h3>')
    .replace(/^### (.+)$/gm,'<h4 class="studio-h4">$1</h4>')
    .replace(/\*\*(.+?)\*\*/g,'<strong>$1</strong>')
    .replace(/^- (.+)$/gm,'<li>$1</li>')
    .replace(/(<li>[\s\S]*?<\/li>)/g,'<ul>$1</ul>')
    .replace(/<\/ul>\s*<ul>/g,'')
    .replace(/\n{2,}/g,'<br>').replace(/\n/g,' ');
}

function renderStudyGuide(out,data){
  if(data.error){out.innerHTML=`<div class="studio-msg studio-error">Coverage Coach error: ${esc(data.error)}</div>`;return;}
  out.innerHTML=`<div class="studio-doc">
    <div class="studio-doc-header"><span class="studio-tag">Study Guide</span><span class="studio-module-label">${esc(data.module)}</span></div>
    <div class="studio-doc-body">${_mdToHtml(data.content)}</div>
  </div>`;
}

function renderCramSheet(out,data){
  if(!data.terms||!data.terms.length){out.innerHTML='<div class="studio-msg">No terms found for this module.</div>';return;}
  const rows=data.terms.map(t=>`<tr><td class="cram-term">${esc(t.term)}</td><td class="cram-def">${esc(t.exam_definition)}<small class="cram-ex"> ${esc(t.example||'')}</small></td></tr>`).join('');
  out.innerHTML=`<div class="studio-doc">
    <div class="studio-doc-header"><span class="studio-tag">Cram Sheet</span><span class="studio-module-label">${esc(data.module)}</span><span class="studio-count">${data.terms.length} terms</span></div>
    <table class="cram-table"><thead><tr><th>Term</th><th>Exam Definition + Example</th></tr></thead><tbody>${rows}</tbody></table>
  </div>`;
}

function renderConceptMap(out,data){
  if(data.error){out.innerHTML=`<div class="studio-msg studio-error">Coverage Coach error: ${esc(data.error)}</div>`;return;}
  out.innerHTML=`<div class="studio-doc">
    <div class="studio-doc-header"><span class="studio-tag">Concept Map</span><span class="studio-module-label">${esc(data.module)}</span></div>
    <pre class="concept-map-box">${esc(data.content||'')}</pre>
  </div>`;
}

function renderPracticeQuiz(out,data){
  if(data.error||!data.questions||!data.questions.length){
    out.innerHTML=`<div class="studio-msg studio-error">${esc(data.error||'No questions generated. Make sure Ollama is running and try again.')}</div>`;return;
  }
  studioQuizState=data.questions.map(()=>null);
  const cards=data.questions.map((q,qi)=>{
    const choices=q.choices.map((c,ci)=>`<button class="qchoice" id="qc-${qi}-${ci}" onclick="answerQ(${qi},${ci})">${String.fromCharCode(65+ci)}. ${esc(c)}</button>`).join('');
    return `<div class="quiz-card" id="qcard-${qi}">
      <p class="quiz-q"><strong>${qi+1}.</strong> ${esc(q.q)}</p>
      <div class="quiz-choices" id="qchoices-${qi}">${choices}</div>
      <div class="quiz-feedback" id="qfeedback-${qi}"></div>
    </div>`;
  }).join('');
  out.innerHTML=`<div class="studio-doc">
    <div class="studio-doc-header"><span class="studio-tag">Practice Quiz</span><span class="studio-module-label">${esc(data.module)}</span><span class="studio-count" id="quiz-score-lbl">0 / ${data.questions.length}</span></div>
    <div id="practice-quiz-cards">${cards}</div>
  </div>`;
  out._quizData=data.questions;
}

function answerQ(qi,ci){
  const out=document.getElementById('studioOutput');
  if(!out||studioQuizState[qi]!==null)return;
  const q=out._quizData[qi];
  studioQuizState[qi]=ci;
  const isCorrect=ci===q.correct;
  const chosen=document.getElementById(`qc-${qi}-${ci}`);
  const correct=document.getElementById(`qc-${qi}-${q.correct}`);
  if(chosen)chosen.classList.add(isCorrect?'qchoice-correct':'qchoice-wrong');
  if(!isCorrect&&correct)correct.classList.add('qchoice-correct');
  [0,1,2,3].forEach(i=>{const b=document.getElementById(`qc-${qi}-${i}`);if(b)b.disabled=true;});
  const fb=document.getElementById(`qfeedback-${qi}`);
  if(fb)fb.innerHTML=`<div class="qfeedback-box ${isCorrect?'qfb-correct':'qfb-wrong'}">${isCorrect?'✓ Correct':'✗ Incorrect'} — ${esc(q.explanation||'')}</div>`;
  const answered=studioQuizState.filter(s=>s!==null).length;
  const correctCount=studioQuizState.filter((s,i)=>s===out._quizData[i]?.correct).length;
  const lbl=document.getElementById('quiz-score-lbl');
  if(lbl)lbl.textContent=`${correctCount} / ${out._quizData.length}`;
  if(answered===out._quizData.length){
    const pct=Math.round(correctCount/out._quizData.length*100);
    const summary=document.createElement('div');
    summary.className=`studio-msg ${pct>=80?'studio-pass':'studio-fail'}`;
    summary.textContent=`Quiz complete: ${correctCount}/${out._quizData.length} correct (${pct}%) ${pct>=80?'✓ Ready for this topic!':'— Review the module and try again.'}`;
    document.getElementById('practice-quiz-cards').appendChild(summary);
  }
}
async function showModules(){app.innerHTML=`<div class="page-wrap"><div class="card"><button onclick="route('dashboard')">← Workspace</button><h1>Course Sources</h1><p class="muted">These are your built-in P&C study sources.</p><div class="grid">${modules.map(m=>`<div class="card"><div class="eyebrow">${m.lesson_count} lessons</div><h2>${esc(m.title)}</h2><p class="muted">${esc(m.description)}</p><button onclick="route('module','${m.slug}')">Open</button></div>`).join('')}</div></div></div>`}
async function showModule(slug){const m=await api('/api/modules/'+slug);app.innerHTML=`<div class="page-wrap"><div class="card"><button onclick="route('dashboard')">← Workspace</button><h1>${esc(m.title)}</h1><p class="muted">${esc(m.description)}</p><div class="list">${m.lessons.map(l=>`<div class="row"><div><strong>${esc(l.title)}</strong><br><span class="muted">${esc(l.summary)}</span></div><button onclick="route('lesson','${l.slug}')">Study</button></div>`).join('')}</div><div class="toolbar"><button onclick="route('quiz','${m.slug}')">Quiz This Module</button><button onclick="quickAsk('Explain the ${esc(m.title)} module and quiz me on it.')">Ask Coverage Coach</button></div></div></div>`}
async function showLesson(slug){
  const l=await api('/api/lessons/'+slug);
  let prev=null,next=null,lessonNum=0,total=0;
  try{
    const mod=await api('/api/modules/'+l.module_slug);
    const ls=mod.lessons||[];total=ls.length;
    const idx=ls.findIndex(x=>x.slug===slug);
    lessonNum=idx+1;
    prev=idx>0?ls[idx-1]:null;
    next=idx<ls.length-1?ls[idx+1]:null;
  }catch(e){}
  const termsHtml=(l.terms&&l.terms.length)
    ?l.terms.map(t=>`<div class="term-card"><strong>${esc(t.term)}</strong><p>${esc(t.exam_definition||t.plain_english_definition)}</p>${t.example?`<small>${esc(t.example)}</small>`:''}</div>`).join('')
    :'<p class="muted">No terms for this module yet.</p>';
  const prevBtn=prev
    ?`<button onclick="route('lesson','${esc(prev.slug)}')">← Previous</button>`
    :`<button disabled>← Previous</button>`;
  const nextBtn=next
    ?`<button class="primary" onclick="completeAndAdvance(${l.id},'${esc(next.slug)}')">Mark Complete &amp; Next →</button>`
    :`<button class="primary" onclick="completeAndDone(${l.id})">Mark Complete ✓</button>`;
  app.innerHTML=`<div class="page-wrap"><article class="lesson card">
    <div class="lesson-nav-top">
      <button onclick="route('module','${esc(l.module_slug)}')">← ${esc(l.module_title||'Module')}</button>
      <span class="lesson-progress">${lessonNum?('Lesson '+lessonNum+' of '+total):''}</span>
    </div>
    <h1>${esc(l.title)}</h1>
    <p class="lesson-summary muted">${esc(l.summary)}</p>
    <div class="lesson-body"><p>${esc(l.body).replace(/\n\n+/g,'</p><p>')}</p></div>
    ${l.example?`<h3>Example</h3><p>${esc(l.example)}</p>`:''}
    ${l.memory_tip?`<h3>Memory tip</h3><p>${esc(l.memory_tip)}</p>`:''}
    <h3>Key terms</h3>
    <div class="term-grid">${termsHtml}</div>
    <details class="lesson-notes-details">
      <summary>Add personal notes (optional)</summary>
      <label>Confidence</label>
      <select id="confidence"><option value="1">Need review</option><option value="2" selected>Getting it</option><option value="3">Strong</option></select>
      <label>Notes</label>
      <textarea id="notes" placeholder="Study notes..."></textarea>
    </details>
    <div class="lesson-nav-bottom">${prevBtn}${nextBtn}</div>
    <div class="lesson-coach">
      <button onclick="speakLesson(${JSON.stringify(l.body||'').replace(/"/g,'&quot;')})">🔊 Listen</button>
      <button onclick="quickAsk('Explain the lesson ${esc(l.title)} and give me one practice question.')">Ask Coverage Coach about this lesson</button>
    </div>
  </article></div>`;
}
async function _saveLessonProgress(id){
  await api('/api/lessons/'+id+'/progress',{method:'POST',body:JSON.stringify({
    completed:true,
    confidence:Number((document.getElementById('confidence')||{}).value||2),
    notes:(document.getElementById('notes')||{}).value||'',
    saved_for_review:false
  })});
}
async function completeAndAdvance(id,nextSlug){await _saveLessonProgress(id);route('lesson',nextSlug);}
async function completeAndDone(id){await _saveLessonProgress(id);toast('Module complete!');showDashboard();}
function speakLesson(text){
  if(!('speechSynthesis' in window)){toast('Read-aloud not supported in this browser');return;}
  speechSynthesis.cancel();
  const u=new SpeechSynthesisUtterance(text);
  u.rate=0.95;
  speechSynthesis.speak(u);
}
async function terms(){const rows=await api('/api/terms');app.innerHTML=`<div class="page-wrap"><div class="card"><button onclick="route('dashboard')">← Workspace</button><h1>Flashcards</h1><div class="list">${rows.map(t=>`<div class="card"><span class="pill">${esc(t.term)}</span><p><strong>Plain English:</strong> ${esc(t.plain_english_definition)}</p><p><strong>Exam:</strong> ${esc(t.exam_definition)}</p>${t.example?`<p class="muted"><strong>Example:</strong> ${esc(t.example)}</p>`:''}</div>`).join('')}</div></div></div>`}
async function quiz(moduleSlug){answers={};currentQuestions=await api('/api/questions?limit=10'+(moduleSlug?'&module_slug='+encodeURIComponent(moduleSlug):''));renderQuiz()}
function renderQuiz(results=null){app.innerHTML=`<div class="page-wrap"><div class="card"><button onclick="route('dashboard')">← Workspace</button><h1>Quiz</h1>${currentQuestions.map((q,i)=>`<div class="card"><div class="eyebrow">Question ${i+1}</div><h3>${esc(q.question_text)}</h3><div class="choices">${q.choices.map(c=>{let cls='choice';const r=results&&results.find(x=>x.question.id===q.id);if(answers[q.id]===c.id)cls+=' selected';if(r&&c.is_correct)cls+=' correct';if(r&&answers[q.id]===c.id&&!r.is_correct)cls+=' wrong';return `<div class="${cls}" onclick="answers[${q.id}]=${c.id};renderQuiz(${results?'lastResults':'null'})">${esc(c.choice_text)}</div>`}).join('')}</div>${results?`<p>${esc((results.find(x=>x.question.id===q.id)||{}).question?.explanation||'')}</p>`:''}</div>`).join('')}<div class="toolbar"><button class="primary" onclick="submitQuiz()">Submit</button><button onclick="quiz()">New Quiz</button></div></div></div>`}
let lastResults=null;
async function submitQuiz(){const out=await api('/api/quiz/submit',{method:'POST',body:JSON.stringify({mode:'practice',answers})});lastResults=out.results;renderQuiz(lastResults);toast('Score: '+out.score+'%')}
async function logout(){await api('/auth/logout',{method:'POST'});location.reload()}
boot();
async function showDashboard(){
  app.innerHTML='<div class="page-wrap"><p style="padding:2rem;text-align:center;color:var(--text-muted)">Loading your dashboard…</p></div>';
  let d;
  try{d=await api('/api/dashboard');}
  catch(e){
    app.innerHTML='<div class="page-wrap"><div class="card"><h2>Dashboard</h2><p>Could not load progress data.</p><button class="primary" onclick="workspace()">Open Workspace →</button></div></div>';
    return;
  }
  const {readiness,lessons,quizzes,mistakes,modules:mods,recommendations:recs,user:uname}=d;
  const ringColor=readiness>=80?'#10b981':readiness>=60?'#f59e0b':'#ef4444';
  const ringLabel=readiness>=80?'✓ Exam Ready':readiness>=60?'↑ Getting There':'⚡ Keep Studying';
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
    :'<li class="dash-no-data">No mistakes yet — great start!</li>';
  const recCards=(recs||[]).slice(0,4).map(r=>
    `<button class="dash-rec-card" onclick="route('lesson','${esc(r.lesson_slug)}')">
      <div class="dash-rec-mod">${esc(r.module_title)}</div>
      <div class="dash-rec-title">${esc(r.lesson_title)}</div>
      <div class="dash-rec-eta">∼${r.estimated_minutes} min →</div>
    </button>`
  ).join('');

  app.innerHTML=`
  <div class="dash-page">
    <header class="dash-topbar-home">
      <span class="dash-brand">◈ P&amp;C Prep Academy</span>
      <button class="primary dash-ws-btn" onclick="workspace()">Workspace →</button>
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
            <div class="dash-stat-num">${quizzes.avg_score||'—'}%</div><div class="dash-stat-lbl">Quiz<br>Average</div></div>
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
          ${mistakes.count>5?'<button class="ghost" onclick="route(\'quiz\')">Practice all mistakes →</button>':''}
        </section>
        ${recCards?`<section class="dash-card dash-half">
          <h2 class="dash-section-title">Up Next</h2>
          <div class="dash-recs">${recCards}</div>
        </section>`:''}
      </div>
    </div>
  </div>`;
}
