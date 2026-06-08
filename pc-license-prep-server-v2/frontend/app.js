const app=document.getElementById('app');
const toastEl=document.getElementById('toast');
let me=null;let modules=[];let currentQuestions=[];let answers={};let chatMessages=[];let studioModuleSlug='';
let voiceEnabled=false;let selectedVoice='af_heart';let voiceHistory=[];let mediaRecorder=null;let isRecording=false;let audioChunks=[];let currentAudio=null;let _voiceInitialized=false;
function toast(msg){toastEl.textContent=msg;toastEl.classList.add('show');setTimeout(()=>toastEl.classList.remove('show'),2200)}
async function api(path,opts={}){const res=await fetch(path,{headers:{'Content-Type':'application/json'},...opts});if(!res.ok){throw new Error(await res.text())}return res.json()}
function esc(s=''){return String(s).replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[m]))}
async function boot(){const m=await api('/api/me');me=m.user;if(!me){return loginScreen()}modules=await api('/api/modules');chatMessages=[];route('dashboard')}
async function loginScreen(){const p=await api('/auth/providers');app.innerHTML=`<section class="login card"><div class="eyebrow">Free public access</div><h1>Sign in to save your progress</h1><p class="muted">Use Google, Microsoft, or Facebook. Local development can use the demo login.</p>${p.providers.map(x=>`<a class="provider" href="/auth/login/${x.id}"><button class="primary provider" ${x.configured?'':'disabled'}>Continue with ${esc(x.name)}${x.configured?'':' — not configured'}</button></a>`).join('')}${p.dev_login_enabled?'<a class="provider" href="/auth/dev-login"><button class="ghost provider">Development Login</button></a>':''}</section>`}
async function route(name,arg){try{if(!me)return loginScreen();if(name==='dashboard')return showDashboard();if(name==='modules')return showModules();if(name==='module')return showModule(arg);if(name==='lesson')return showLesson(arg);if(name==='terms')return terms();if(name==='quiz')return quiz(arg);if(name==='coach')return workspace();if(name==='plan')return showPlan();if(name==='diagnostic')return showDiagnostic()}catch(e){app.innerHTML=`<div class="page-wrap"><div class="card"><h2>Something went wrong</h2><p>${esc(e.message)}</p></div></div>`}}
function sourcePanel(){
  const opts=modules.map(m=>`<option value="${esc(m.slug)}"${m.slug===studioModuleSlug?' selected':''}>${esc(m.title)}</option>`).join('');
  return `<aside class="pane ref-pane"><div class="pane-head"><h2>📚 Quick Reference</h2><select class="studio-module-select ref-module-select" id="refModuleSelect" onchange="studioModuleSlug=this.value;_loadRefTerms(this.value)"><option value="">— pick a module —</option>${opts}</select></div><div class="pane-body" id="refPaneBody"><div class="ref-loading">Select a module to load its key terms.</div></div></aside>`;
}
async function _loadRefTerms(slug){
  const body=document.getElementById('refPaneBody');
  if(!body)return;
  if(!slug){body.innerHTML='<div class="ref-loading">Select a module to load its key terms.</div>';return;}
  body.innerHTML='<div class="ref-loading">Loading terms…</div>';
  try{
    const terms=await api('/api/terms?module_slug='+encodeURIComponent(slug));
    if(!terms||!terms.length){body.innerHTML='<div class="ref-loading">No terms for this module yet.</div>';return;}
    body.innerHTML=`<div class="ref-terms">${terms.map(t=>`<div class="ref-term"><strong>${esc(t.term)}</strong><p>${esc(t.exam_definition||t.plain_english_definition)}</p></div>`).join('')}</div>`;
  }catch(e){body.innerHTML='<div class="ref-loading">Could not load terms.</div>';}
}
function chatPanel(){
  const defaultIntro=`<div class="message assistant intro"><p>Hi! I'm <strong>Coverage Coach</strong>, your P&amp;C licensing study tutor. I know the full course — every lesson, term, and concept.</p><p>Ask me to explain a tricky topic, quiz you on key terms, compare coverages, or tell you where to focus before the exam. Use the <strong>Studio panel →</strong> to generate study guides, cram sheets, and practice quizzes.</p><p>What do you want to work on today?</p></div>`;
  const voiceControlsHtml=voiceEnabled?`<div class="voice-controls"><select class="voice-select" id="voiceSelect" onchange="selectedVoice=this.value">${(window._voiceList||[selectedVoice]).map(v=>`<option value="${esc(v)}"${v===selectedVoice?' selected':''}>${esc(v)}</option>`).join('')}</select><button class="ptt-btn${isRecording?' recording':''}" id="pttBtn" onmousedown="startRecording()" onmouseup="stopRecordingAndSend()" onmouseleave="isRecording&&stopRecordingAndSend()" ontouchstart="startRecording()" ontouchend="stopRecordingAndSend()">${isRecording?'🔴 Recording…':'🎤 Hold to Talk'}</button><button class="stop-btn icon-btn" onclick="stopAudio()" title="Stop playback">⏹</button></div><div class="voice-status" id="voiceStatus">Ready</div>`:'';
  return `<section class="pane center"><div class="pane-head"><h2>Chat</h2><div class="pane-tools"><button class="icon-btn">⋮</button></div></div><div class="pane-body chat-body"><div class="messages" id="messages">${defaultIntro}${chatMessages.map(m=>`<div class="message ${m.role}">${esc(m.text)}</div>`).join('')}</div><div class="suggestions"><button onclick="quickAsk('Am I ready for the real thing?')">Am I ready for the real thing?</button><button onclick="quickAsk('What are the most commonly missed topics on the P&amp;C exam?')">Most commonly missed P&amp;C exam topics</button><button onclick="quickAsk('Explain the difference between replacement cost and actual cash value')">Replacement cost vs. actual cash value</button><button onclick="quickAsk('Quiz me on the most important terms I need to know')">Quiz me on important terms</button></div><div class="composer"><textarea id="coachQuestion" placeholder="Ask a question or create something"></textarea><span class="composer-meta">0 sources</span><button class="send-btn" onclick="askCoach()">➜</button></div><div class="voice-toolbar"><button class="voice-toggle-btn${voiceEnabled?' active':''}" onclick="toggleVoice()">${voiceEnabled?'🔴 Voice On':'🎙️ Voice Coach'}</button>${voiceControlsHtml}</div></div></section>`;
}
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
async function workspace(){app.innerHTML=`<div class="workspace"><div class="ws-topbar"><button class="ws-back-btn" onclick="showDashboard()">← Dashboard</button><span class="ws-topbar-title">◈ Study Workspace</span></div><div class="ws-panels">${sourcePanel()}${chatPanel()}${studioPanel()}</div></div>`;scrollMessages();if(typeof studioModuleSlug!=='undefined'&&!studioModuleSlug&&modules.length){studioModuleSlug=modules[0].slug;const sel=document.getElementById('studioModuleSelect');if(sel)sel.value=studioModuleSlug;const ref=document.getElementById('refModuleSelect');if(ref)ref.value=studioModuleSlug;}_loadRefTerms(studioModuleSlug);}
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
  // Dim all choices first, then highlight chosen and correct
  [0,1,2,3].forEach(i=>{const b=document.getElementById(`qc-${qi}-${i}`);if(b){b.disabled=true;b.classList.add('qchoice-dim');}});
  if(chosen){chosen.classList.remove('qchoice-dim');chosen.classList.add(isCorrect?'qchoice-correct':'qchoice-wrong');chosen.textContent=(isCorrect?'✓ ':'✗ ')+chosen.textContent;}
  if(!isCorrect&&correct){correct.classList.remove('qchoice-dim');correct.classList.add('qchoice-correct');correct.textContent='✓ '+correct.textContent;}
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
async function showDiagnostic(){
  app.innerHTML='<div class="page-wrap"><p style="padding:2rem;text-align:center;color:var(--text-muted)">Loading placement quiz…</p></div>';
  let qs;
  try{qs=await api('/api/diagnostic/questions');}
  catch(e){app.innerHTML=`<div class="page-wrap"><div class="card"><button onclick="route('dashboard')">← Dashboard</button><h2>Placement Quiz</h2><p>Could not load questions.</p></div></div>`;return;}
  const diagAnswers={};
  function _renderDiag(){
    const allAnswered=qs.every(q=>diagAnswers[q.id]!=null);
    const cards=qs.map((q,qi)=>{
      const answered=diagAnswers[q.id]!=null;
      const choices=q.choices.map(c=>{
        let cls='diag-choice';
        if(answered){
          if(diagAnswers[q.id]===c.id)cls+=' diag-selected';
          else cls+=' diag-dimmed';
        }
        return `<button class="${cls}" ${answered?'disabled':''} onclick="_diagAnswer(${qi},${c.id})">${esc(c.choice_text)}</button>`;
      }).join('');
      return `<div class="diag-card${answered?' diag-card-done':''}">
        <div class="diag-q-meta"><span class="diag-q-mod">${esc(q.module_title)}</span><span class="diag-q-num">Q${qi+1} of ${qs.length}</span></div>
        <p class="diag-q-text"><strong>${qi+1}.</strong> ${esc(q.question_text)}</p>
        <div class="diag-choices">${choices}</div>
      </div>`;
    }).join('');
    app.innerHTML=`<div class="page-wrap diagnostic-page">
      <div class="card" style="max-width:780px;margin:0 auto">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:18px">
          <button onclick="route('dashboard')">← Dashboard</button>
          <span style="font-size:.82rem;color:var(--text-muted);font-weight:600">Placement Quiz · ${qs.filter(q=>diagAnswers[q.id]!=null).length} / ${qs.length} answered</span>
        </div>
        <h2 style="margin:0 0 4px">Where do you stand?</h2>
        <p class="muted" style="margin:0 0 20px;font-size:.88rem">Answer all 5 questions, then submit to personalize your study plan.</p>
        <div id="diagCards">${cards}</div>
        ${allAnswered?'<div style="text-align:center;margin-top:24px"><button class="primary" style="font-size:1rem;padding:12px 28px" onclick="_diagSubmit()">Submit &amp; See My Plan →</button></div>':''}
      </div>
    </div>`;
  }
  window._diagAnswer=function(qi,choiceId){diagAnswers[qs[qi].id]=choiceId;_renderDiag();};
  window._diagSubmit=async function(){
    app.innerHTML='<div class="page-wrap"><p style="padding:2rem;text-align:center;color:var(--text-muted)">Submitting…</p></div>';
    try{
      const result=await api('/api/diagnostic/submit',{method:'POST',body:JSON.stringify({answers:diagAnswers})});
      sessionStorage.setItem('diagnosticScore',JSON.stringify(result));
    }catch(e){toast('Could not submit — please try again.');}
    route('plan');
  };
  _renderDiag();
}
async function showPlan(){
  app.innerHTML='<div class="page-wrap"><p style="padding:2rem;text-align:center;color:var(--text-muted)">Loading your study plan…</p></div>';
  // Load data-only summary first (fast), then fetch the full plan with Ollama narrative in background
  let base;
  try{base=await api('/api/study-plan/summary');}
  catch(e){
    app.innerHTML=`<div class="page-wrap"><div class="card"><button onclick="route('dashboard')">← Dashboard</button><h2>Study Plan</h2><p>Could not load plan.</p></div></div>`;
    return;
  }
  const {summary,plan}=base;
  function _renderPlanSteps(steps){
    const TYPE_ICONS={spaced_review:'🔁',weak_module:'⚡',confidence_gap:'🎯',start_here:'▶',finish_module:'✅'};
    return steps.length
      ?steps.map((step,i)=>`<div class="plan-step-card">
          <div class="plan-step-num">${i+1}</div>
          <div class="plan-step-body">
            <div class="plan-step-icon">${TYPE_ICONS[step.type]||'📚'}</div>
            <div class="plan-step-info">
              <div class="plan-step-title">${esc(step.module_title)}</div>
              <div class="plan-step-reason">${esc(step.reason)}</div>
            </div>
            <button class="primary plan-step-btn" onclick="route('module','${esc(step.module_slug)}')">${esc(step.action_label)} →</button>
          </div>
        </div>`).join('')
      :'<p class="dash-empty">No plan items yet — complete some lessons and quizzes first.</p>';
  }
  // Render page immediately (no Ollama wait)
  app.innerHTML=`
  <div class="dash-page">
    <header class="dash-topbar-home">
      <span class="dash-brand">◈ P&amp;C Prep Academy</span>
      <button class="ghost" onclick="route('dashboard')">← Dashboard</button>
    </header>
    <div class="dash-wrap">
      <h1 class="dash-welcome">Your Adaptive Study Plan</h1>
      ${(()=>{const raw=sessionStorage.getItem('diagnosticScore');if(!raw)return '';sessionStorage.removeItem('diagnosticScore');try{const r=JSON.parse(raw);const ms=r.module_scores||{};const strong=Object.entries(ms).filter(([,v])=>v===1).map(([k])=>k.replace(/-/g,' ')).join(', ');const focus=Object.entries(ms).filter(([,v])=>v===0).map(([k])=>k.replace(/-/g,' ')).join(', ');return `<div class="diagnostic-results-banner"><span class="diag-banner-score">✅ Placement complete: You scored ${r.score}/${r.total}</span>${strong?`<span class="diag-banner-strong">💪 Strong foundation: ${esc(strong)}</span>`:''}${focus?`<span class="diag-banner-focus">🎯 Focus areas: ${esc(focus)}</span>`:''}<span class="diag-banner-tail">Your plan has been personalized based on your results.</span></div>`;}catch(e){return '';}})()}
      <div class="plan-summary-bar">
        <div class="plan-stat"><div class="plan-stat-num">${summary.modules_mastered}</div><div class="plan-stat-lbl">Modules<br>Mastered</div></div>
        <div class="plan-stat"><div class="plan-stat-num">${summary.modules_total}</div><div class="plan-stat-lbl">Total<br>Modules</div></div>
        <div class="plan-stat${summary.overall_readiness>=80?' stat-pass':summary.overall_readiness>=60?' stat-warn':''}"><div class="plan-stat-num">${summary.overall_readiness}%</div><div class="plan-stat-lbl">Quiz<br>Average</div></div>
        <div class="plan-stat${summary.review_items_due>0?' stat-warn':''}"><div class="plan-stat-num">${summary.review_items_due}</div><div class="plan-stat-lbl">Review<br>Due</div></div>
      </div>
      <div class="plan-narrative card" id="planNarrative"><span class="plan-narrative-spinner">Coverage Coach is writing your plan…</span></div>
      <section class="dash-section">
        <h2 class="dash-section-title">Priority Actions</h2>
        <div class="plan-steps" id="planSteps">${_renderPlanSteps(plan)}</div>
      </section>
      <div class="dash-bottom">
        <section class="dash-card dash-half">
          <h2 class="dash-section-title">Weak Areas</h2>
          <ul class="plan-area-list" id="planWeak"><li class="plan-area-item plan-muted">Loading…</li></ul>
        </section>
        <section class="dash-card dash-half">
          <h2 class="dash-section-title">Strengths</h2>
          <ul class="plan-area-list" id="planStrong"><li class="plan-area-item plan-muted">Loading…</li></ul>
        </section>
      </div>
    </div>
  </div>`;
  // Fetch full plan (with Ollama narrative) in background and inject when ready
  api('/api/study-plan').then(full=>{
    const narEl=document.getElementById('planNarrative');
    if(narEl)narEl.textContent=full.narrative||'';
    const stepsEl=document.getElementById('planSteps');
    if(stepsEl)stepsEl.innerHTML=_renderPlanSteps(full.plan||[]);
    const weakEl=document.getElementById('planWeak');
    if(weakEl)weakEl.innerHTML=full.weak_areas&&full.weak_areas.length
      ?full.weak_areas.map(w=>`<li class="plan-area-item plan-weak"><span class="plan-area-name">${esc(w.title)}</span><span class="plan-area-pct">${w.accuracy}%</span></li>`).join('')
      :'<li class="plan-area-item plan-muted">No weak areas yet</li>';
    const strongEl=document.getElementById('planStrong');
    if(strongEl)strongEl.innerHTML=full.strengths&&full.strengths.length
      ?full.strengths.map(s=>`<li class="plan-area-item plan-strong"><span class="plan-area-name">${esc(s.title)}</span><span class="plan-area-pct">${s.accuracy}%</span></li>`).join('')
      :'<li class="plan-area-item plan-muted">Keep studying to earn strengths!</li>';
  }).catch(()=>{
    const narEl=document.getElementById('planNarrative');
    if(narEl)narEl.textContent='Coverage Coach is offline — narrative unavailable.';
    const weakEl=document.getElementById('planWeak');if(weakEl)weakEl.innerHTML='<li class="plan-area-item plan-muted">—</li>';
    const strongEl=document.getElementById('planStrong');if(strongEl)strongEl.innerHTML='<li class="plan-area-item plan-muted">—</li>';
  });
}
async function toggleVoice(){
  if(!voiceEnabled){
    await initVoice();
  } else {
    voiceEnabled=false;
    stopAudio();
    if(mediaRecorder&&isRecording){try{mediaRecorder.stop();}catch(e){} isRecording=false;}
    const panel=document.querySelector('.pane.center');if(panel)panel.outerHTML=chatPanel();
    scrollMessages();
  }
}
async function initVoice(){
  if(!_voiceInitialized){
    try{
      const list=await fetch('http://localhost:8001/voices').then(r=>{if(!r.ok)throw new Error('HTTP '+r.status);return r.json();});
      window._voiceList=list;
      if(list.length&&!list.includes(selectedVoice))selectedVoice=list[0];
      _voiceInitialized=true;
    }catch(e){
      setVoiceStatus('Voice service offline — run scripts/start_voice_service.sh');
      toast('Voice service unreachable');
      return;
    }
  }
  voiceEnabled=true;
  const panel=document.querySelector('.pane.center');if(panel)panel.outerHTML=chatPanel();
  scrollMessages();
  setVoiceStatus('Ready');
}
async function startRecording(){
  if(isRecording)return;
  try{
    const stream=await navigator.mediaDevices.getUserMedia({audio:true});
    audioChunks=[];
    mediaRecorder=new MediaRecorder(stream,{mimeType:'audio/webm'});
    mediaRecorder.ondataavailable=e=>{if(e.data.size>0)audioChunks.push(e.data);};
    mediaRecorder.start();
    isRecording=true;
    const btn=document.getElementById('pttBtn');
    if(btn){btn.textContent='🔴 Recording…';btn.classList.add('recording');}
    setVoiceStatus('Recording…');
  }catch(e){
    toast('Microphone access denied');
    setVoiceStatus('Microphone error — check browser permissions');
  }
}
async function stopRecordingAndSend(){
  if(!isRecording||!mediaRecorder)return;
  isRecording=false;
  const btn=document.getElementById('pttBtn');
  if(btn){btn.textContent='🎤 Hold to Talk';btn.classList.remove('recording');}
  setVoiceStatus('Transcribing…');
  await new Promise(resolve=>{
    mediaRecorder.onstop=resolve;
    mediaRecorder.stop();
    mediaRecorder.stream.getTracks().forEach(t=>t.stop());
  });
  const blob=new Blob(audioChunks,{type:'audio/webm'});
  audioChunks=[];
  const fd=new FormData();
  fd.append('audio',blob,'recording.webm');
  fd.append('voice',selectedVoice);
  fd.append('conversation_history',JSON.stringify(voiceHistory.slice(-6)));
  setVoiceStatus('Coach is thinking…');
  try{
    const resp=await fetch('http://localhost:8001/chat',{method:'POST',body:fd});
    if(!resp.ok){const txt=await resp.text();throw new Error(txt);}
    const data=await resp.json();
    if(data.error==='no_speech'){setVoiceStatus('No speech detected — try again');return;}
    chatMessages.push({role:'user',text:data.transcript});
    chatMessages.push({role:'assistant',text:data.response_text});
    voiceHistory.push({role:'user',content:data.transcript});
    voiceHistory.push({role:'assistant',content:data.response_text});
    if(voiceHistory.length>6)voiceHistory=voiceHistory.slice(-6);
    // Re-render messages pane only (keep voice toolbar state)
    const msgEl=document.getElementById('messages');
    if(msgEl){
      const defaultIntro=document.querySelector('.message.assistant.intro');
      const introHtml=defaultIntro?defaultIntro.outerHTML:'';
      msgEl.innerHTML=introHtml+chatMessages.map(m=>`<div class="message ${m.role}">${esc(m.text)}</div>`).join('');
    }
    scrollMessages();
    playAudioBase64(data.audio_base64);
  }catch(e){
    setVoiceStatus('Error: '+String(e).slice(0,80));
    toast('Voice chat error');
  }
}
function stopAudio(){
  if(currentAudio){currentAudio.pause();currentAudio=null;}
  setVoiceStatus('Ready');
}
function setVoiceStatus(msg){
  const el=document.getElementById('voiceStatus');
  if(el)el.textContent=msg;
}
function playAudioBase64(base64wav){
  stopAudio();
  const binary=atob(base64wav);
  const bytes=new Uint8Array(binary.length);
  for(let i=0;i<binary.length;i++)bytes[i]=binary.charCodeAt(i);
  const blob=new Blob([bytes],{type:'audio/wav'});
  const url=URL.createObjectURL(blob);
  currentAudio=new Audio(url);
  currentAudio.onended=()=>{URL.revokeObjectURL(url);setVoiceStatus('Ready');};
  currentAudio.play();
  setVoiceStatus('Speaking…');
}
boot();
async function showDashboard(){
  app.innerHTML='<div class="page-wrap"><p style="padding:2rem;text-align:center;color:var(--text-muted)">Loading your dashboard…</p></div>';
  let d,planData;
  try{d=await api('/api/dashboard');}
  catch(e){
    app.innerHTML='<div class="page-wrap"><div class="card"><h2>Dashboard</h2><p>Could not load progress data.</p><button class="primary" onclick="workspace()">Open Workspace →</button></div></div>';
    return;
  }
  try{planData=await api('/api/study-plan/summary');}catch(e){planData=null;}
  let diagStatus=null;
  try{diagStatus=await api('/api/diagnostic/status');}catch(e){}
  // Show prompt if: status fetch failed (new user) OR explicitly not completed; suppress only if skipped this session
  const showDiagPrompt=(!diagStatus||!diagStatus.completed)&&sessionStorage.getItem('diagnosticSkipped')!=='true';
  const {readiness,lessons,quizzes,mistakes,modules:mods,recommendations:recs,user:uname}=d;
  const ringColor=readiness>=80?'#10b981':readiness>=60?'#f59e0b':'#ef4444';
  const ringLabel=readiness>=80?'✓ Exam Ready':readiness>=60?'↑ Getting There':'⚡ Keep Studying';
  const circ=(2*Math.PI*40);
  const dash=(circ*readiness/100).toFixed(1);
  const ring=`<svg class="dash-ring-svg" viewBox="0 0 100 100">
    <circle cx="50" cy="50" r="40" fill="none" stroke="var(--border)" stroke-width="8"/>
    <circle cx="50" cy="50" r="40" fill="none" stroke="${ringColor}" stroke-width="8"
      stroke-dasharray="${dash} ${circ.toFixed(1)}" stroke-linecap="round"
      transform="rotate(-90 50 50)" style="transition:stroke-dasharray .6s"/>
    <text x="50" y="47" text-anchor="middle" font-size="22" font-weight="700" fill="${ringColor}">${readiness}%</text>
    <text x="50" y="61" text-anchor="middle" font-size="6" fill="var(--text-muted)" style="text-transform:uppercase;letter-spacing:2px">READINESS</text>
  </svg>`;
  const bars=quizzes.recent.length
    ?quizzes.recent.slice().reverse().map(q=>{
        const h=Math.max(8,Math.round(q.score*.65)),c=q.score>=80?'#10b981':q.score>=60?'#f59e0b':'#ef4444';
        return `<div class="dash-bar-wrap" title="${q.score}%"><div class="dash-bar" style="height:${h}px;background:${c}"></div><span class="dash-bar-lbl">${q.score}</span></div>`;
      }).join('')
    :'<p class="dash-empty-sm">No quizzes yet</p>';
  const modCards=mods.map(m=>{
    const dc=m.pct===100?'#10b981':m.pct>0?'#6366f1':'var(--text-muted)';
    return `<button class="dash-mod-card${m.pct===100?' dash-mod-card-done':''}" onclick="route('module','${esc(m.slug)}')">
      <div class="dash-mod-hdr"><span class="dash-mod-name">${esc(m.title)}</span><span class="dash-mod-pct" style="color:${dc}">${m.pct}%</span></div>
      <div class="dash-progbar"><div class="dash-progfill${m.pct===100?' dash-progfull':''}" style="width:${Math.max(m.pct,2)}%"></div></div>
      <div class="dash-mod-meta">${m.completed_lessons} / ${m.total_lessons} lessons</div>
    </button>`;
  }).join('');
  const mistakeItems=mistakes.top.length
    ?mistakes.top.map(m=>{const q=m.question.length>80?m.question.slice(0,80)+'…':m.question;return `<li class="dash-mistake-item"><span class="dash-miss-badge">✗ ${m.times_missed}\xd7</span><span class="dash-miss-q">${esc(q)}</span></li>`;}).join('')
    :'<li class="dash-no-data">No mistakes yet — great start!</li>';
  const recCards=(recs||[]).slice(0,4).map(r=>
    `<button class="dash-rec-card" onclick="route('lesson','${esc(r.lesson_slug)}')">
      <div class="dash-rec-mod">${esc(r.module_title)}</div>
      <div class="dash-rec-title">${esc(r.lesson_title)}</div>
      <div class="dash-rec-eta">∼${r.estimated_minutes} min &nbsp;<span style="color:var(--accent,#6366f1);font-weight:700">Start →</span></div>
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
      <p class="dash-welcome-sub">Here's your study snapshot for today.</p>
      ${showDiagPrompt?`<div class="diagnostic-prompt-card">
        <div class="diag-prompt-body">
          <div class="diag-prompt-icon">📋</div>
          <div class="diag-prompt-text">
            <strong>Quick Placement Quiz</strong>
            <span class="diag-prompt-sub">Find out where to focus — 5 questions, 2 minutes.</span>
          </div>
        </div>
        <div class="diag-prompt-actions">
          <button class="primary" onclick="route('diagnostic')">Start Placement Quiz →</button>
          <button class="ghost" onclick="sessionStorage.setItem('diagnosticSkipped','true');this.closest('.diagnostic-prompt-card').remove()">Skip for now</button>
        </div>
      </div>`:''}
      ${planData&&planData.plan&&planData.plan.length?`<div class="plan-dash-card">
        <div class="plan-dash-hdr"><span class="plan-dash-title" style="font-size:.8rem;text-transform:uppercase;letter-spacing:.1em;color:var(--text-muted);font-weight:700">📋 Study Plan</span><button class="ghost plan-dash-link" onclick="route('plan')">View full plan →</button></div>
        <div class="plan-dash-steps">${planData.plan.slice(0,2).map((s,i)=>`<div class="plan-dash-step"><span class="plan-dash-num">${i+1}</span><div class="plan-dash-info"><strong>${esc(s.module_title)}</strong><span class="plan-dash-reason">${esc(s.reason.slice(0,80))}${s.reason.length>80?'…':''}</span></div><button class="primary plan-dash-action" onclick="route('module','${esc(s.module_slug)}')">${esc(s.action_label)} →</button></div>`).join('')}</div>
      </div>`:''}
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
        <h2 class="dash-section-title">📊 Module Progress</h2>
        <div class="dash-mod-grid">${modCards||'<p class="dash-empty">No modules loaded yet.</p>'}</div>
      </section>
      <div class="dash-bottom">
        <section class="dash-card dash-half">
          <h2 class="dash-section-title">📝 Mistake Bank <span class="dash-pill">${mistakes.count}</span></h2>
          <ul class="dash-mistake-list">${mistakeItems}</ul>
          ${mistakes.count>5?'<button class="ghost" onclick="route(\'quiz\')">Practice all mistakes →</button>':''}
        </section>
        ${recCards?`<section class="dash-card dash-half">
          <h2 class="dash-section-title">🎯 Up Next</h2>
          <div class="dash-recs">${recCards}</div>
        </section>`:''}
      </div>
    </div>
  </div>`;
}
