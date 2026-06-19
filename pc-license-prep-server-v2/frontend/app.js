const app=document.getElementById('app');
const toastEl=document.getElementById('toast');
let me=null;let modules=[];let currentQuestions=[];let answers={};let chatMessages=[];
function toast(msg){toastEl.textContent=msg;toastEl.classList.add('show');setTimeout(()=>toastEl.classList.remove('show'),2200)}
async function api(path,opts={}){const res=await fetch(path,{headers:{'Content-Type':'application/json'},...opts});if(!res.ok){throw new Error(await res.text())}return res.json()}
function esc(s=''){return String(s).replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[m]))}
async function boot(){const m=await api('/api/me');me=m.user;if(!me){return loginScreen()}if(!me.course||!me.state){return courseSelector()}if(!me.state){return stateSelector()}modules=await api('/api/modules');chatMessages=[];route('dashboard')}
async function courseSelector(opts={}){
  const courses=[
    {id:'pc',icon:'🏠',title:'Property & Casualty',sub:'P&C License Exam Prep',detail:'14 modules · 90 lessons'},
    {id:'lh',icon:'❤️',title:'Life & Health',sub:'L&H License Exam Prep',detail:'14 modules · 90+ lessons'}
  ];
  app.innerHTML=`<div class="course-sel-page"><div class="course-sel-card"><h1 class="course-sel-title">What are you studying for?</h1><p class="course-sel-sub">Choose your license track. You can switch anytime.</p><div class="course-sel-grid">${courses.map(c=>`<button class="course-opt${c.id===(me&&me.course)?'  course-opt-active':''}" onclick="pickCourse('${c.id}')"><span class="course-opt-icon">${c.icon}</span><span class="course-opt-title">${esc(c.title)}</span><span class="course-opt-sub">${esc(c.sub)}</span><span class="course-opt-detail">${esc(c.detail)}</span></button>`).join('')}</div>${opts.switchable?'<button class="ghost" style="margin-top:1rem" onclick="showDashboard()">← Back to dashboard</button>':''}</div></div>`;
}
async function pickCourse(courseId){
  const res=await api('/api/me/course',{method:'POST',body:JSON.stringify({course:courseId})});
  me.course=res.course;
  modules=await api('/api/modules');
  chatMessages=[];
  if(!me.state){return stateSelector();}
  route('dashboard');
}
const _US_STATES=[['AL','Alabama'],['AK','Alaska'],['AZ','Arizona'],['AR','Arkansas'],['CA','California'],['CO','Colorado'],['CT','Connecticut'],['DE','Delaware'],['DC','District of Columbia'],['FL','Florida'],['GA','Georgia'],['HI','Hawaii'],['ID','Idaho'],['IL','Illinois'],['IN','Indiana'],['IA','Iowa'],['KS','Kansas'],['KY','Kentucky'],['LA','Louisiana'],['ME','Maine'],['MD','Maryland'],['MA','Massachusetts'],['MI','Michigan'],['MN','Minnesota'],['MS','Mississippi'],['MO','Missouri'],['MT','Montana'],['NE','Nebraska'],['NV','Nevada'],['NH','New Hampshire'],['NJ','New Jersey'],['NM','New Mexico'],['NY','New York'],['NC','North Carolina'],['ND','North Dakota'],['OH','Ohio'],['OK','Oklahoma'],['OR','Oregon'],['PA','Pennsylvania'],['RI','Rhode Island'],['SC','South Carolina'],['SD','South Dakota'],['TN','Tennessee'],['TX','Texas'],['UT','Utah'],['VT','Vermont'],['VA','Virginia'],['WA','Washington'],['WV','West Virginia'],['WI','Wisconsin'],['WY','Wyoming']];
function stateSelector(opts={}){
  const opts2=opts||{};
  const sel=_US_STATES.map(([a,n])=>`<option value="${a}"${me&&me.state===a?' selected':''}>${n}</option>`).join('');
  app.innerHTML=`<div class="course-sel-page"><div class="course-sel-card"><h1 class="course-sel-title">What state are you getting licensed in?</h1><p class="course-sel-sub">We'll show your exam structure, vendor, and state-specific topics.</p><select id="stateDropdown" class="state-dropdown"><option value="">— Select your state —</option>${sel}</select><button class="primary" style="width:100%;margin-top:1rem" onclick="pickState()">Continue →</button><br><button class="ghost" style="margin-top:.5rem;font-size:.85rem;color:var(--muted)" onclick="${opts2.dashboard?'showDashboard()':'skipState()'}">Skip for now</button>${opts2.back?'<br><button class="ghost" style="margin-top:.25rem;font-size:.85rem" onclick="showDashboard()">← Back</button>':''}</div></div>`;
}
async function pickState(){
  const val=document.getElementById('stateDropdown')?.value;
  if(!val){toast('Please select a state first');return;}
  const res=await api('/api/me/state',{method:'POST',body:JSON.stringify({state:val})});
  me.state=res.state;me.state_name=res.state_name;
  modules=await api('/api/modules');chatMessages=[];
  route('dashboard');
}
async function skipState(){modules=await api('/api/modules');chatMessages=[];route('dashboard')}
async function loginScreen(){
  const p=await api('/auth/providers');
  const providerBtns=p.providers.filter(x=>x.configured).map(x=>{
    const icons={
      google:`<svg width="20" height="20" viewBox="0 0 48 48"><path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.06 17.74 9.5 24 9.5z"/><path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"/><path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"/><path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-3.56-13.47-8.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"/></svg>`,
      microsoft:`<svg width="20" height="20" viewBox="0 0 21 21"><rect x="1" y="1" width="9" height="9" fill="#f25022"/><rect x="11" y="1" width="9" height="9" fill="#7fba00"/><rect x="1" y="11" width="9" height="9" fill="#00a4ef"/><rect x="11" y="11" width="9" height="9" fill="#ffb900"/></svg>`
    };
    const labels={google:'Sign in with Google',microsoft:'Sign in with Microsoft'};
    return `<a href="/auth/login/${x.id}" class="oauth-btn oauth-btn-${x.id}">${icons[x.id]||''}<span>${labels[x.id]||'Sign in with '+esc(x.name)}</span></a>`;
  }).join('');
  const devBtn=p.dev_login_enabled?`<div class="oauth-divider"><span>or</span></div><a href="/auth/dev-login" class="oauth-btn oauth-btn-dev"><span>Development Login</span></a>`:'';
  app.innerHTML=`<div class="login-page"><section class="login-card"><div class="login-logo">◈</div><h1 class="login-title">P&amp;C Prep Academy</h1><p class="login-sub">Sign in to track your progress toward your license</p><div class="login-btns">${providerBtns}${devBtn}</div><p class="login-fine">By signing in you agree to our <a href="/terms">Terms of Use</a> and <a href="/privacy">Privacy Policy</a>.</p></section></div>`;
}
async function route(name,arg){try{if(!me)return loginScreen();if(name==='dashboard')return showDashboard();if(name==='modules')return showModules();if(name==='module')return showModule(arg);if(name==='lesson')return showLesson(arg);if(name==='terms')return terms();if(name==='quiz')return quiz(arg);if(name==='coach')return workspace()}catch(e){app.innerHTML=`<div class="page-wrap"><div class="card"><h2>Something went wrong</h2><p>${esc(e.message)}</p></div></div>`}}
function sourcePanel(){const courseLabel=me&&me.course==='lh'?'Life & Health':'Property & Casualty';return `<aside class="pane"><div class="pane-head"><h2>Sources</h2><span class="course-badge" onclick="courseSelector()" title="Switch course" style="cursor:pointer;font-size:.75rem;padding:2px 8px;border-radius:12px;background:var(--accent-muted,#e8f0fe);color:var(--accent,#1a73e8);margin-left:8px">${esc(courseLabel)}</span><div class="pane-tools"><button class="icon-btn">▣</button></div></div><div class="pane-body"><button class="ghost" style="width:100%;font-size:1rem;margin-bottom:20px" onclick="route('modules')">＋ Add sources</button><div class="source-search"><input placeholder="Search the web for new sources"><div class="source-actions"><button>🌐 Web⌄</button><button>✦ Fast Research⌄</button><button class="icon-btn" style="margin-left:auto">⌕</button></div></div><div class="empty-state"><div><div class="big">▧</div><strong>Saved sources will appear here</strong><p>Click Add source above to add PDFs, websites, text, videos, or audio files. Or import a file directly from Google Drive.</p></div></div></div></aside>`}
function chatPanel(){
  const intro = chatMessages.length === 0
    ? `<div class="message assistant intro">
        <p>👋 Hi! I'm <strong>Coverage Coach</strong> — your AI insurance exam tutor.</p>
        <p>Ask me anything about insurance concepts, exam terms, state law, or practice questions. I'm here to help you pass.</p>
        <p class="muted" style="font-size:.85rem">I only answer insurance licensing questions. Up to 20 questions/hour.</p>
      </div>`
    : '';
  return `<section class="pane center">
    <div class="pane-head"><h2>Coverage Coach</h2><div class="pane-tools"><button class="icon-btn" onclick="chatMessages=[];workspace()" title="Clear chat">✕</button></div></div>
    <div class="pane-body chat-body">
      <div class="messages" id="messages">${intro}${chatMessages.map(m=>`<div class="message ${m.role}">${esc(m.text)}</div>`).join('')}</div>
      <div class="suggestions">
        <button onclick="quickAsk('What is the difference between a peril and a hazard?')">Peril vs hazard?</button>
        <button onclick="quickAsk('Explain coinsurance and how the penalty works')">Coinsurance penalty?</button>
        <button onclick="quickAsk('What does subrogation mean in insurance?')">What is subrogation?</button>
      </div>
      <div class="composer">
        <textarea id="coachQuestion" placeholder="Ask Coverage Coach an insurance question…"></textarea>
        <button class="send-btn" onclick="askCoach()">➜</button>
      </div>
    </div>
  </section>`;
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
let _wsPanel='chat';
function _wsTab(p){_wsPanel=p;const panels=document.querySelectorAll('.ws-panels>.pane');const tabs=document.querySelectorAll('.ws-mob-tab');const order=['sources','chat','studio'];panels.forEach((el,i)=>{el.classList.toggle('ws-pane-hidden',order[i]!==p)});tabs.forEach(t=>{t.classList.toggle('ws-mob-tab-active',t.dataset.p===p)})}
async function workspace(){
  app.innerHTML=`<div class="workspace"><div class="ws-topbar"><button class="ws-back-btn" onclick="showDashboard()">← Dashboard</button><span class="ws-topbar-title">◈ Study Workspace</span></div><div class="ws-panels">${sourcePanel()}${chatPanel()}${studioPanel()}</div><nav class="ws-mob-nav"><button class="ws-mob-tab" data-p="sources" onclick="_wsTab('sources')">📚 Reference</button><button class="ws-mob-tab ws-mob-tab-active" data-p="chat" onclick="_wsTab('chat')">💬 Chat</button><button class="ws-mob-tab" data-p="studio" onclick="_wsTab('studio')">✦ Studio</button></nav></div>`;
  _wsTab(_wsPanel);
  scrollMessages();
  renderStateBanner();
  if(typeof studioModuleSlug!=='undefined'&&!studioModuleSlug&&modules.length){studioModuleSlug=modules[0].slug;const sel=document.getElementById('studioModuleSelect');if(sel)sel.value=studioModuleSlug;}
}
async function renderStateBanner(){
  const head=document.querySelector('.pane.center .pane-head');
  if(!head)return;
  const existing=head.nextElementSibling;
  if(existing&&existing.classList.contains('state-banner'))existing.remove();
  if(me&&me.state){
    let info=null;
    try{info=await api('/api/state-info/'+me.state)}catch(e){}
    if(info){
      const exam=me.course==='lh'?info.lh_exam:info.pc_exam;
      const banner=document.createElement('div');
      banner.className='state-banner';
      banner.innerHTML=`<span>📍 <strong>${esc(info.state_name)}</strong> · ${esc(info.vendor)} · ${exam.total_scored} questions · ${exam.passing_score}% to pass</span><button class="ghost" style="font-size:.8rem;padding:2px 8px" onclick="toggleStateTopics(this,${JSON.stringify(JSON.stringify(info.state_topics||[]))})">Topics ▾</button><button class="ghost" style="font-size:.8rem;padding:2px 8px" onclick="stateSelector({dashboard:true,back:true})">Change</button>`;
      head.after(banner);
    }
  }else{
    const banner=document.createElement('div');
    banner.className='state-banner state-banner-empty';
    banner.innerHTML=`<button class="ghost" style="font-size:.85rem" onclick="stateSelector()">📍 Select your state to see exam details →</button>`;
    head.after(banner);
  }
}
function toggleStateTopics(btn,topicsJson){
  const topics=JSON.parse(topicsJson);
  const existing=btn.parentElement.nextElementSibling;
  if(existing&&existing.classList.contains('state-topics')){existing.remove();btn.textContent='Topics ▾';return}
  const div=document.createElement('div');div.className='state-topics';
  div.innerHTML=`<ul>${topics.map(t=>`<li>${esc(t)}</li>`).join('')}</ul>`;
  btn.parentElement.after(div);btn.textContent='Topics ▴';
}
function scrollMessages(){setTimeout(()=>{const el=document.getElementById('messages');if(el)el.scrollTop=el.scrollHeight},50)}
function quickAsk(text){const q=document.getElementById('coachQuestion');if(q){q.value=text;askCoach()}else{chatMessages.push({role:'user',text});route('dashboard').then(()=>askCoachText(text))}}
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
  api('/api/studio/generate','POST',{action,module_slug:studioModuleSlug})
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
    <div class="lesson-coach"><button onclick="quickAsk('Explain the lesson ${esc(l.title)} and give me one practice question.')">Ask Coverage Coach about this lesson</button></div>
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

  const course=me&&me.course==='lh'?'lh':'pc';
  const stInfo=me&&me.state?await api('/api/state-info/'+me.state).catch(()=>null):null;
  const examKey=course==='lh'?'lh_exam':'pc_exam';
  const examData=stInfo&&stInfo[examKey];
  const stateBanner=stInfo
    ?`<div class="state-banner" id="stateBanner">
        <span class="state-banner-loc">📍 <strong>${esc(stInfo.state_name)}</strong> <span class="state-banner-vendor">(${esc(stInfo.vendor)})</span></span>
        <span class="state-banner-sep">·</span>
        <span class="state-banner-exam">${course==='lh'?'L&H':'P&C'}: ${examData?examData.total_scored+' questions · '+examData.passing_score+'% to pass':'—'}</span>
        <span class="state-banner-sep">·</span>
        <button class="state-banner-btn" onclick="document.getElementById('stateTopics').classList.toggle('state-topics-open')">State topics ▾</button>
        <button class="state-banner-btn" onclick="stateSelector({dashboard:true,back:true})">Change state</button>
        <div class="state-topics" id="stateTopics"><ul>${(stInfo.state_topics||[]).map(t=>`<li>${esc(t)}</li>`).join('')}</ul>${stInfo.outline_url?`<a href="${esc(stInfo.outline_url)}" target="_blank" rel="noopener" class="state-outline-link">View official exam outline →</a>`:''}</div>
      </div>`
    :`<div class="state-banner state-banner-empty"><span>📍 </span><button class="state-banner-btn" onclick="stateSelector({dashboard:true,back:true})">Select your state to see your exam details →</button></div>`;

  app.innerHTML=`
  <div class="dash-page">
    <header class="dash-topbar-home">
      <span class="dash-brand">◈ ${me&&me.course==='lh'?'L&amp;H':'P&amp;C'} Prep Academy <button class="course-switch-link" onclick="courseSelector({switchable:true})">Switch</button></span>
      <div style="display:flex;align-items:center;gap:.6rem">
        <button class="primary dash-ws-btn" onclick="workspace()">Workspace →</button>
        <button class="ghost signout-btn" onclick="logout()" title="Sign out">Sign out</button>
      </div>
    </header>
    ${stateBanner}
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

// ── VOICE / TTS ───────────────────────────────────────────────────────────────

const VOICE_SERVICE = 'http://localhost:8001';

async function loadVoices() {
  try {
    const res = await fetch(VOICE_SERVICE + '/voices');
    const data = await res.json();
    const sel = document.getElementById('voiceSelect');
    if (!sel) return;
    sel.innerHTML = data.voices.map(v =>
      `<option value="${esc(v.id)}" ${v.id === data.default ? 'selected' : ''}>
        ${esc(v.name)} — ${esc(v.description)}
      </option>`
    ).join('');
  } catch(e) {
    console.warn('Voice service not available:', e);
  }
}

async function speakText(text, voiceId, language) {
  const voice = voiceId || 'Ryan';
  const lang = language || 'English';
  try {
    const res = await fetch(VOICE_SERVICE + '/tts', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({text, voice, language: lang, instruct: ''})
    });
    if (!res.ok) throw new Error('TTS request failed: ' + res.status);
    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    const audio = new Audio(url);
    audio.onended = () => URL.revokeObjectURL(url);
    audio.play();
    return audio;
  } catch(e) {
    console.warn('TTS playback error:', e);
    return null;
  }
}
