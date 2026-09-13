function getAnonId(){
  let id = localStorage.getItem('wit_anon_id');
  if(!id){
    id = (crypto.randomUUID && crypto.randomUUID()) ||
         ('anon-' + Date.now() + '-' + Math.random().toString(36).slice(2));
    localStorage.setItem('wit_anon_id', id);
  }
  return id;
}
const app=document.getElementById('app');
const toastEl=document.getElementById('toast');
let me=null;let modules=[];let currentQuestions=[];let answers={};let chatMessages=[];let studioModuleSlug=null;let currentQuizIndex=0;let flashcardIndex=0;let flashcardFlipped=false;
let flashcardRows=[];
let quizContext={moduleSlug:null,mistakesOnly:false};
let quizSubmitting=false;
let lessonSavePending=false;
let studioQuizState=[];
function toast(msg){toastEl.textContent=msg;toastEl.classList.add('show');setTimeout(()=>toastEl.classList.remove('show'),2200)}
async function api(path,opts={}){const res=await fetch(path,{credentials:'include',...opts,headers:{'Content-Type':'application/json','X-Anon-Id':getAnonId(),...(opts.headers||{})}});if(!res.ok){throw new Error(await res.text())}return res.json()}
function esc(s=''){return String(s).replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[m]))}
function cleanTitle(raw){
  if(!raw)return'WIT Radio Live';
  let t=raw.replace(/\.mp3$/i,'');
  t=t.replace(/^(morning_acoustic|day_shift|dance_party|night_shift)_/,'');
  t=t.replace(/^(hip_hop|rnb|edm|pop)_/,'');
  t=t.replace(/^[a-z][-a-z]*_/,'');
  t=t.replace(/^\d{2,3}_/,'');
  t=t.replace(/_\d{3}$/,'');
  t=t.replace(/_/g,' ').replace(/\b\w/g,c=>c.toUpperCase()).trim();
  return t||'WIT Radio Live';
}
async function boot(){
  const m = await api('/api/me');
  me = m.user;
  if(!me.course || !me.state){ return courseSelector(); }
  modules = await api('/api/modules');
  chatMessages = [];
  route('dashboard');
}
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
  studioModuleSlug=null;
  modules=await api('/api/modules');
  chatMessages=[];
  if(!me.state){return stateSelector();}
  route('dashboard');
}
const _US_STATES=[['AL','Alabama'],['AK','Alaska'],['AZ','Arizona'],['AR','Arkansas'],['CA','California'],['CO','Colorado'],['CT','Connecticut'],['DE','Delaware'],['DC','District of Columbia'],['FL','Florida'],['GA','Georgia'],['HI','Hawaii'],['ID','Idaho'],['IL','Illinois'],['IN','Indiana'],['IA','Iowa'],['KS','Kansas'],['KY','Kentucky'],['LA','Louisiana'],['ME','Maine'],['MD','Maryland'],['MA','Massachusetts'],['MI','Michigan'],['MN','Minnesota'],['MS','Mississippi'],['MO','Missouri'],['MT','Montana'],['NE','Nebraska'],['NV','Nevada'],['NH','New Hampshire'],['NJ','New Jersey'],['NM','New Mexico'],['NY','New York'],['NC','North Carolina'],['ND','North Dakota'],['OH','Ohio'],['OK','Oklahoma'],['OR','Oregon'],['PA','Pennsylvania'],['RI','Rhode Island'],['SC','South Carolina'],['SD','South Dakota'],['TN','Tennessee'],['TX','Texas'],['UT','Utah'],['VT','Vermont'],['VA','Virginia'],['WA','Washington'],['WV','West Virginia'],['WI','Wisconsin'],['WY','Wyoming']];
function stateSelector(opts={}){
  const opts2=opts||{};
  const sel=_US_STATES.map(([a,n])=>`<option value="${a}"${me&&me.state===a?' selected':''}>${n}</option>`).join('');
  app.innerHTML=`<div class="course-sel-page"><div class="course-sel-card"><h1 class="course-sel-title">What state are you getting licensed in?</h1><p class="course-sel-sub">Choose your study jurisdiction. Verified exam details are shown where available.</p><select id="stateDropdown" class="state-dropdown"><option value="">— Select your state —</option>${sel}</select><button class="primary" style="width:100%;margin-top:1rem" onclick="pickState()">Continue →</button><br><button class="ghost" style="margin-top:.5rem;font-size:.85rem;color:var(--muted)" onclick="${opts2.dashboard?'showDashboard()':'skipState()'}">Skip for now</button>${opts2.back?'<br><button class="ghost" style="margin-top:.25rem;font-size:.85rem" onclick="showDashboard()">← Back</button>':''}</div></div>`;
}
async function pickState(){
  const val=document.getElementById('stateDropdown')?.value;
  if(!val){toast('Please select a state first');return;}
  const res=await api('/api/me/state',{method:'POST',body:JSON.stringify({state:val})});
  me.state=res.state;me.state_name=res.state_name;
  studioModuleSlug=null;
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
  app.innerHTML=`<div class="login-page"><section class="login-card"><div class="login-logo">◈</div><h1 class="login-title">P&amp;C Prep Academy</h1><p class="login-sub">Sign in to track your progress toward your license</p><div class="login-btns">${providerBtns}</div><p class="login-fine">By signing in you agree to our <a href="/terms">Terms of Use</a> and <a href="/privacy">Privacy Policy</a>.</p></section></div>`;
}
async function route(name,arg){try{if(name!=='coach')app.classList.remove('ws-locked');if(name==='dashboard')return await showDashboard();if(name==='modules')return await showModules();if(name==='module')return await showModule(arg);if(name==='lesson')return await showLesson(arg);if(name==='terms')return await terms(arg);if(name==='exam')return await timedExamSetup();if(name==='quiz')return await quiz(arg);if(name==='coach')return await workspace()}catch(e){app.innerHTML=`<div class="page-wrap"><div class="card"><h2>Something went wrong</h2><p>${esc(e.message)}</p><button onclick="route('dashboard')">Back to dashboard</button></div></div>`}}
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
    <button class="studio-tile tile-flash" onclick="route('terms',studioModuleSlug||undefined)"><span>▧<br>Flashcards</span><b>›</b></button>
    <button class="studio-tile tile-exam"  onclick="route('exam')"><span>▢<br>Timed Practice</span><b>›</b></button>
  </div>
  <div class="studio-output" id="studioOutput">
    <div class="studio-empty"><div class="spark">✦</div>
    <strong>Pick a module and a tile to generate study content.</strong>
    <p>Study Guide and Practice Quiz use Coverage Coach (Ollama). Cram Sheet is instant.</p></div>
  </div></div></aside>`}
let _wsPanel='chat';
function _wsTab(p){_wsPanel=p;const panels=document.querySelectorAll('.ws-panels>.pane');const tabs=document.querySelectorAll('.ws-mob-tab');const order=['sources','chat','studio'];panels.forEach((el,i)=>{el.classList.toggle('ws-pane-hidden',order[i]!==p)});tabs.forEach(t=>{t.classList.toggle('ws-mob-tab-active',t.dataset.p===p)})}
async function workspace(){
  app.classList.add('ws-locked');
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

      const banner=document.createElement('div');
      banner.className='state-banner';
      banner.innerHTML=`<span>📍 <strong>${esc(info.state_name)}</strong> · ${esc(info.vendor)} · ${esc(examProfileSummary(info,me.course))}</span>${info.outline_url?`<a href="${esc(info.outline_url)}" target="_blank" rel="noopener">Source handbook</a>`:''}<span class="muted">State-law content review pending</span><button class="ghost" style="font-size:.8rem;padding:2px 8px" onclick="stateSelector({dashboard:true,back:true})">Change</button>`;
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
  const valid=Array.isArray(data.questions)&&data.questions.length&&data.questions.every(q=>
    q&&typeof q.q==='string'&&Array.isArray(q.choices)&&q.choices.length>=2&&
    q.choices.every(c=>typeof c==='string')&&Number.isInteger(q.correct)&&q.correct>=0&&q.correct<q.choices.length);
  if(data.error||!valid){
    out.innerHTML=`<div class="studio-msg studio-error">${esc(data.error||'No questions generated. Make sure Ollama is running and try again.')}</div>`;return;
  }
  // Generated and fallback quizzes also need shuffled choices. Carry the
  // correct choice through the shuffle instead of retaining its old index.
  data={...data,questions:data.questions.map(q=>{
    const choices=q.choices.map((text,index)=>({text,correct:index===q.correct}));
    for(let i=choices.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[choices[i],choices[j]]=[choices[j],choices[i]];}
    return {...q,choices:choices.map(c=>c.text),correct:choices.findIndex(c=>c.correct)};
  })};
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
async function showModules(){app.innerHTML=`<div class="page-wrap"><div class="card"><button onclick="route('dashboard')">← Dashboard</button><h1>Your Course</h1><p class="muted">Study material for ${me&&me.course==='lh'?'Life & Health':'Property & Casualty'}${me&&me.state_name?' in '+esc(me.state_name):''}.</p><div class="grid">${modules.map(m=>`<div class="card"><div class="eyebrow">${m.lesson_count} lessons</div><h2>${esc(m.title)}</h2><p class="muted">${esc(m.description)}</p><button onclick="route('module','${m.slug}')">Open</button></div>`).join('')}</div></div></div>`}
async function showModule(slug){const m=await api('/api/modules/'+slug);app.innerHTML=`<div class="page-wrap"><div class="card"><button onclick="route('dashboard')">← Workspace</button><h1>${esc(m.title)}</h1>${m.is_state_law?'<p>State-law material awaits review against current official sources.</p>':''}<p class="muted">${esc(m.description)}</p><div class="list">${m.lessons.map(l=>`<div class="row"><div><strong>${esc(l.title)}</strong><br><span class="muted">${esc(l.summary)}</span></div><button onclick="route('lesson','${l.slug}')">Study</button></div>`).join('')}</div><div class="toolbar"><button onclick="route('quiz','${m.slug}')">Quiz This Module</button><button onclick="quickAsk('Explain the ${esc(m.title)} module and quiz me on it.')">Ask Coverage Coach</button></div></div></div>`}
async function showLesson(slug){
  const l=await api('/api/lessons/'+slug);
  const saved=l.progress||{completed:false,confidence:0,notes:'',saved_for_review:false};
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
    ?`<button class="primary" data-lesson-save onclick="completeAndAdvance(${l.id},'${esc(next.slug)}')">Mark Complete &amp; Next →</button>`
    :`<button class="primary" data-lesson-save onclick="completeAndDone(${l.id})">Mark Complete ✓</button>`;
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
    <details class="lesson-notes-details"${saved.notes||saved.saved_for_review?' open':''}>
      <summary>Add personal notes (optional)</summary>
      <label for="confidence">Confidence</label>
      <select id="confidence">${['Not rated','Need review','Getting it','Strong'].map((label,value)=>`<option value="${value}"${value===saved.confidence?' selected':''}>${label}</option>`).join('')}</select>
      <label for="notes">Notes</label>
      <textarea id="notes" maxlength="5000" placeholder="Study notes...">${esc(saved.notes||'')}</textarea>
      <label class="lesson-review-label"><input type="checkbox" id="savedForReview"${saved.saved_for_review?' checked':''}> Save this lesson for review</label>
      <button data-lesson-save onclick="saveLessonNotes(${l.id})">Save notes</button>
      <span id="lessonSaveStatus" role="status" aria-live="polite"></span>
    </details>
    <div class="lesson-nav-bottom">${prevBtn}${nextBtn}</div>
    <div class="lesson-coach"><button onclick="quickAsk('Explain the lesson ${esc(l.title)} and give me one practice question.')">Ask Coverage Coach about this lesson</button></div>
  </article></div>`;
}
async function _saveLessonProgress(id,completed){
  if(lessonSavePending)return false;
  const notes=document.getElementById('notes');
  if(!notes)return false;
  const payload={
    confidence:Number(document.getElementById('confidence').value),
    notes:notes.value,
    saved_for_review:document.getElementById('savedForReview').checked
  };
  if(completed!==undefined)payload.completed=completed;
  lessonSavePending=true;
  const buttons=[...document.querySelectorAll('[data-lesson-save]')];
  const status=document.getElementById('lessonSaveStatus');
  buttons.forEach(b=>b.disabled=true);
  if(status)status.textContent='Saving…';
  try{
    await api('/api/lessons/'+id+'/progress',{method:'POST',body:JSON.stringify(payload)});
    if(status)status.textContent='Saved';
    return true;
  }catch(e){
    if(status)status.textContent='Could not save. Your notes are still here; please try again.';
    return false;
  }finally{lessonSavePending=false;buttons.forEach(b=>b.disabled=false);}
}
async function saveLessonNotes(id){await _saveLessonProgress(id);}
async function completeAndAdvance(id,nextSlug){if(await _saveLessonProgress(id,true))await route('lesson',nextSlug);}
async function completeAndDone(id){if(await _saveLessonProgress(id,true)){toast('Lesson complete!');await route('dashboard');}}
async function terms(moduleSlug){
  const rows=await api('/api/terms'+(moduleSlug?'?module_slug='+encodeURIComponent(moduleSlug):''));
  if(!rows.length){app.innerHTML=`<div class="page-wrap"><div class="card"><button onclick="route('dashboard')">← Dashboard</button><p>No flashcards yet.</p></div></div>`;return;}
  flashcardRows=rows;flashcardIndex=0;flashcardFlipped=false;renderFlashcard();
}
function flipFlashcard(){flashcardFlipped=!flashcardFlipped;renderFlashcard();document.querySelector('.flashcard')?.focus();}
function moveFlashcard(index){flashcardIndex=Math.max(0,Math.min(index,flashcardRows.length-1));flashcardFlipped=false;renderFlashcard();}
function renderFlashcard(){
  const rows=flashcardRows;
  if(!rows.length)return;
  const t=rows[flashcardIndex];
  const progress=`${flashcardIndex+1} of ${rows.length}`;
  app.innerHTML=`<div class="page-wrap"><div class="card">
    <button onclick="route('dashboard')">← Dashboard</button>
    <h1>Flashcards</h1>
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:1rem">
      <div class="eyebrow">${progress}</div>
      <div class="progress-bar" style="width:200px;height:6px;background:var(--border);border-radius:3px">
        <div style="width:${((flashcardIndex+1)/rows.length*100)}%;height:100%;background:var(--accent);border-radius:3px"></div>
      </div>
    </div>
    <div class="flashcard" role="button" tabindex="0" aria-label="${flashcardFlipped?'Show term':'Reveal definition'}" onclick="flipFlashcard()" onkeydown="if(event.key==='Enter'||event.key===' '){event.preventDefault();flipFlashcard()}" style="cursor:pointer;min-height:200px;padding:2rem;background:var(--surface);border:2px solid var(--border);border-radius:16px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;transition:all .2s">
      ${!flashcardFlipped
        ?`<div class="pill" style="margin-bottom:1rem">${esc(t.term)}</div><p class="muted">Tap to reveal definition</p>`
        :`<p><strong>Plain English:</strong> ${esc(t.plain_english_definition)}</p>
           <p style="margin-top:1rem"><strong>Exam:</strong> ${esc(t.exam_definition)}</p>
           ${t.example?`<p class="muted" style="margin-top:1rem"><strong>Example:</strong> ${esc(t.example)}</p>`:''}`
      }
    </div>
    <div class="toolbar" style="margin-top:1.5rem">
      ${flashcardIndex>0?`<button onclick="moveFlashcard(${flashcardIndex-1})">← Prev</button>`:'<span></span>'}
      ${flashcardIndex<rows.length-1
        ?`<button class="primary" onclick="moveFlashcard(${flashcardIndex+1})">Next →</button>`
        :`<button class="primary" onclick="moveFlashcard(0)">Start Over</button>`
      }
    </div>
  </div></div>`;
}
async function quiz(moduleSlug,{mistakesOnly=false}={}){
  app.classList.remove('ws-locked');
  quizContext={moduleSlug:moduleSlug||null,mistakesOnly};
  answers={};currentQuizIndex=0;currentQuestions=[];quizSubmitting=false;
  app.innerHTML='<div class="page-wrap"><p role="status">Loading your questions…</p></div>';
  try{
    currentQuestions=await api('/api/questions?limit=10'+(moduleSlug?'&module_slug='+encodeURIComponent(moduleSlug):'')+(mistakesOnly?'&mistakes_only=true':''));
    renderQuiz();
  }catch(e){
    app.innerHTML='<div class="page-wrap"><div class="card"><h1>Could not load questions</h1><p>Please try again.</p><button onclick="restartQuiz()">Try again</button><button onclick="route(\'dashboard\')">Dashboard</button></div></div>';
  }
}
async function practiceMistakes(){await quiz(null,{mistakesOnly:true});}
async function restartQuiz(){await quiz(quizContext.moduleSlug,{mistakesOnly:quizContext.mistakesOnly});}
function renderQuiz(results=null){
  if(results){
    const resultsById=new Map(results.map(r=>[r.question.id,r]));
    const orderedResults=currentQuestions.map(q=>resultsById.get(q.id)).filter(Boolean);
    const score=orderedResults.filter(r=>r.is_correct).length;
    const total=orderedResults.length;
    if(!total){toast('No quiz results returned. Please try again.');return;}
    const pct=Math.round(score/total*100);
    app.innerHTML=`<div class="page-wrap"><div class="card">
      <button onclick="route('dashboard')">← Dashboard</button>
      <h1>Quiz Results</h1>
      <div class="quiz-score" style="font-size:2rem;font-weight:700;margin:1rem 0;color:${pct>=70?'#10b981':'#ef4444'}">${pct}% — ${score}/${total} correct</div>
      <div class="list">${orderedResults.map(r=>{
        const q=r.question;
        const displayed=currentQuestions.find(item=>item.id===q.id);
        const choicesById=new Map(q.choices.map(c=>[c.id,c]));
        const choices=displayed.choices.map(c=>choicesById.get(c.id)).filter(Boolean);
        return `<div class="card" style="border-left:4px solid ${r.is_correct?'#10b981':'#ef4444'}">
          <div class="eyebrow">${r.is_correct?'✓ Correct':'✗ Incorrect'}</div>
          <p><strong>${esc(q.question_text)}</strong></p>
          <ul class="quiz-answer-review">${choices.map(c=>`<li class="${c.is_correct?'answer-correct':''}"><strong>${esc(c.choice_text)}</strong>${c.id===r.selected_choice_id?' <span>(Your answer)</span>':''}${c.is_correct?' <span>✓ Correct answer</span>':''}${c.explanation?`<p>${esc(c.explanation)}</p>`:''}</li>`).join('')}</ul>
          <p class="muted">${esc(q.explanation||'')}</p>
        </div>`;
      }).join('')}</div>
      <div class="toolbar">
        <button class="primary" onclick="restartQuiz()">${quizContext.mistakesOnly?'Continue mistake review':'New Quiz'}</button>
        <button onclick="route('dashboard')">Dashboard</button>
      </div>
    </div></div>`;
    return;
  }
  const q=currentQuestions[currentQuizIndex];
  if(!q){
    app.innerHTML=`<div class="page-wrap"><div class="card"><h1>${quizContext.mistakesOnly?'Mistake review':'Practice quiz'}</h1><p>${quizContext.mistakesOnly?'You have no mistakes to review in this course and state.':'No practice questions are available for this selection yet.'}</p><button onclick="route('dashboard')">Back to dashboard</button></div></div>`;
    return;
  }
  const progress=`${currentQuizIndex+1} of ${currentQuestions.length}`;
  app.innerHTML=`<div class="page-wrap"><div class="card">
    <button onclick="route('dashboard')">← Dashboard</button>
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:1rem">
      <div class="eyebrow">Question ${progress}</div>
      <div class="progress-bar" style="width:200px;height:6px;background:var(--border);border-radius:3px">
        <div style="width:${((currentQuizIndex+1)/currentQuestions.length*100)}%;height:100%;background:var(--accent);border-radius:3px;transition:width .3s"></div>
      </div>
    </div>
    <h3 style="margin-bottom:1.5rem">${esc(q.question_text)}</h3>
    <div class="choices">${q.choices.map(c=>`
      <button type="button" class="choice${answers[q.id]===c.id?' selected':''}" aria-pressed="${answers[q.id]===c.id}" onclick="answers[${q.id}]=${c.id};renderQuiz()">
        ${esc(c.choice_text)}
      </button>`).join('')}
    </div>
    <div class="toolbar" style="margin-top:1.5rem">
      ${currentQuizIndex>0?`<button onclick="currentQuizIndex--;renderQuiz()">← Back</button>`:''}
      ${answers[q.id]!=null
        ?currentQuizIndex<currentQuestions.length-1
          ?`<button class="primary" onclick="currentQuizIndex++;renderQuiz()">Next →</button>`
          :`<button id="submitQuizButton" class="primary" onclick="submitQuiz()">Submit Quiz</button>`
        :`<button class="primary" disabled>Select an answer</button>`
      }
    </div>
  </div></div>`;
}
let lastResults=null;
async function submitQuiz(){
  if(quizSubmitting)return;
  if(!currentQuestions.length||currentQuestions.some(q=>!q.choices.some(c=>c.id===answers[q.id]))){toast('Answer every question before submitting.');return;}
  quizSubmitting=true;
  const button=document.getElementById('submitQuizButton');
  if(button){button.disabled=true;button.textContent='Submitting…';}
  try{
    const out=await api('/api/quiz/submit',{method:'POST',body:JSON.stringify({mode:quizContext.mistakesOnly?'mistakes':'practice',answers})});
    lastResults=out.results;renderQuiz(lastResults);toast('Score: '+out.score+'%');
  }catch(e){toast('Could not submit. Your answers are still here; please try again.');}
  finally{quizSubmitting=false;if(button){button.disabled=false;button.textContent='Submit Quiz';}}
}
function logout(){
  if(!confirm('Reset your progress? This clears your saved study data on this browser.')) return;
  localStorage.removeItem('wit_anon_id');
  location.reload();
}
boot();
async function showDashboard(){app.classList.remove('ws-locked');
  app.innerHTML='<div class="page-wrap"><p style="padding:2rem;text-align:center;color:var(--text-muted)">Loading your dashboard…</p></div>';
  let d;
  try{d=await api('/api/dashboard');}
  catch(e){
    app.innerHTML='<div class="page-wrap"><div class="card"><h2>Dashboard</h2><p>Could not load progress data.</p><button class="primary" onclick="workspace()">Open Workspace →</button></div></div>';
    return;
  }
  const {readiness,lessons,quizzes,mistakes,modules:mods,recommendations:recs,user:uname}=d;
  const ringColor=readiness>=80?'#10b981':readiness>=60?'#f59e0b':'#ef4444';
  const ringLabel=readiness>=80?'✓ Strong progress':readiness>=60?'↑ Making progress':'⚡ Keep studying';
  const circ=(2*Math.PI*40);
  const dash=(circ*readiness/100).toFixed(1);
  const ring=`<svg class="dash-ring-svg" viewBox="0 0 100 100">
    <circle cx="50" cy="50" r="40" fill="none" stroke="var(--border)" stroke-width="10"/>
    <circle cx="50" cy="50" r="40" fill="none" stroke="${ringColor}" stroke-width="10"
      stroke-dasharray="${dash} ${circ.toFixed(1)}" stroke-linecap="round"
      transform="rotate(-90 50 50)" style="transition:stroke-dasharray .6s"/>
    <text x="50" y="46" text-anchor="middle" font-size="20" font-weight="700" fill="${ringColor}">${readiness}%</text>
    <text x="50" y="62" text-anchor="middle" font-size="7" fill="var(--text-muted)">Study progress</text>
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
  const stateBanner=stInfo
    ?`<div class="state-banner" id="stateBanner">
        <span class="state-banner-loc">📍 <strong>${esc(stInfo.state_name)}</strong> <span class="state-banner-vendor">(${esc(stInfo.vendor)})</span></span>
        <span class="state-banner-sep">·</span>
        <span class="state-banner-exam">${course==='lh'?'L&H':'P&C'}: ${esc(examProfileSummary(stInfo,course))}</span>
        <span class="state-banner-sep">·</span>
        <button class="state-banner-btn" onclick="document.getElementById('stateTopics').classList.toggle('state-topics-open')">State topics ▾</button>
        <button class="state-banner-btn" onclick="stateSelector({dashboard:true,back:true})">Change state</button>
        <div class="state-topics" id="stateTopics"><p>State-law question review is pending.</p><ul>${(stInfo.state_topics||[]).map(t=>`<li>${esc(t)}</li>`).join('')}</ul>${stInfo.outline_url?`<a href="${esc(stInfo.outline_url)}" target="_blank" rel="noopener" class="state-outline-link">View source handbook →</a>`:''}</div>
      </div>`
    :`<div class="state-banner state-banner-empty"><span>📍 </span><button class="state-banner-btn" onclick="stateSelector({dashboard:true,back:true})">Select your state to see your exam details →</button></div>`;

  app.innerHTML=`
  <div class="dash-page">
    <header class="dash-topbar-home">
      <span class="dash-brand">◈ ${me&&me.course==='lh'?'L&amp;H':'P&amp;C'} Prep Academy <button class="course-switch-link" onclick="courseSelector({switchable:true})">Switch</button></span>
      <div style="display:flex;align-items:center;gap:.6rem">
        <button class="primary dash-ws-btn" onclick="workspace()">Workspace →</button>
        <button class="ghost signout-btn" onclick="logout()" title="Reset progress">Reset progress</button>
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
          ${mistakes.count>0?'<button class="ghost" onclick="practiceMistakes()">Practice missed questions →</button>':''}
        </section>
        ${recCards?`<section class="dash-card dash-half">
          <h2 class="dash-section-title">Up Next</h2>
          <div class="dash-recs">${recCards}</div>
        </section>`:''}
      </div>
      <div class="dash-footer" style="text-align:center;margin-top:2rem;padding:1rem 0;font-size:.8rem;color:var(--muted);border-top:1px solid var(--border)">
        <a href="/privacy" target="_blank" style="color:var(--muted)">Privacy Policy</a> ·
        <a href="/terms" target="_blank" style="color:var(--muted)">Terms of Service</a> ·
        <span>Free because it's the right thing to do.</span>
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

function examProfileSummary(info,course){
  const profiles=(info.profiles||[]).filter(p=>p.course===course);
  if(!profiles.length)return 'Exam format awaiting verification';
  return profiles.map(p=>`${p.name}: ${p.scored_questions} scored + up to ${p.pretest_questions_max} pretest, ${p.duration_minutes} min; passing scaled score ${p.passing_score}`).join(' · ') + ` (checked ${info.reviewed_at})`;
}

let timedExam=null, timedIndex=0, timedBusy=false, timedClock=null, timedOffset=0;
async function timedExamSetup(){
  clearInterval(timedClock);
  const data=await api('/api/exams/active');
  timedExam=data.exam;
  app.innerHTML=`<div class="page-wrap"><div class="card"><h1>Timed practice</h1>
    <p>50 questions · 60 minutes · ${esc(me.course==='lh'?'Life & Health':'Property & Casualty')}</p>
    <p>Practice across general course topics. This session excludes state law and does not reproduce an official exam's topic weights or passing score.</p>
    <p>Answers save as you go. The clock keeps running when you leave. Unanswered questions count as incorrect.</p>
    ${timedExam?`<p>Your ${esc(timedExam.course.toUpperCase())} session is ${timedExam.status==='completed'?'finished':'in progress'}.</p><button class="primary" onclick="openTimedExam()">${timedExam.status==='completed'?'View results':'Resume session'}</button>`:''}
    ${!timedExam||timedExam.status==='completed'?'<button class="primary" id="startTimedExam" onclick="startTimedExam()">Start 60-minute session</button>':''}
    <button onclick="route('coach')">Back to workspace</button><p id="timedError" role="alert"></p></div></div>`;
}
async function startTimedExam(){
  const button=document.getElementById('startTimedExam');if(button)button.disabled=true;
  try{timedExam=await api('/api/exams',{method:'POST'});timedIndex=0;openTimedExam()}
  catch(e){document.getElementById('timedError').textContent=e.message;if(button)button.disabled=false}
}
function openTimedExam(){
  timedOffset=Date.parse(timedExam.server_now)-Date.now();
  timedIndex=Math.min(timedIndex,timedExam.questions.length-1);
  renderTimedExam();
  clearInterval(timedClock);
  if(timedExam.status!=='completed')timedClock=setInterval(tickTimedExam,1000);
}
function renderTimedExam(){
  if(timedExam.status==='completed'){
    clearInterval(timedClock);
    const result=timedExam.result;
    app.innerHTML=`<div class="page-wrap"><div class="card"><h1>Practice results</h1>
      <h2>${result.correct} / ${timedExam.total_questions} · ${result.percent}%</h2><p>${esc(timedExam.notice)}</p>
      <h3>Topic results</h3><ul>${Object.entries(result.module_scores).map(([name,r])=>`<li>${esc(name)}: ${r.correct} / ${r.total}</li>`).join('')}</ul>
      <button onclick="route('exam')">Another session</button><button onclick="route('coach')">Back to study</button>
      ${timedExam.questions.map((q,i)=>`<details class="exam-result"><summary>${i+1}. ${q.is_correct?'Correct':q.selected_choice_id?'Incorrect':'Unanswered'} — ${esc(q.question_text)}</summary><ul>${q.choices.map(c=>`<li>${esc(c.choice_text)}${c.id===q.selected_choice_id?' (your answer)':''}${c.is_correct?' (correct)':''}${c.explanation?` — ${esc(c.explanation)}`:''}</li>`).join('')}</ul><p>${esc(q.explanation)}</p></details>`).join('')}
      </div></div>`;return;
  }
  const q=timedExam.questions[timedIndex];
  const selected=timedExam.answers[String(q.id)];
  app.innerHTML=`<div class="page-wrap"><div class="card"><h1>Timed practice</h1>
    <p><strong id="examTimer" role="timer"></strong> remaining · ${Object.keys(timedExam.answers).length} / ${timedExam.total_questions} answered</p>
    <p class="muted">${esc(timedExam.course.toUpperCase())} · General practice; state law excluded</p>
    <nav class="exam-grid" aria-label="Question navigation">${timedExam.questions.map((item,i)=>`<button ${timedBusy?'disabled':''} class="${i===timedIndex?'active':''}" aria-label="Question ${i+1}${timedExam.answers[String(item.id)]?' answered':''}${timedExam.flagged.includes(item.id)?' flagged':''}" onclick="timedIndex=${i};renderTimedExam()">${i+1}${timedExam.flagged.includes(item.id)?' ⚑':timedExam.answers[String(item.id)]?' ✓':''}</button>`).join('')}</nav>
    <h2>Question ${timedIndex+1}</h2><p>${esc(q.question_text)}</p>
    <div class="exam-choices">${q.choices.map(c=>`<button ${timedBusy?'disabled':''} aria-pressed="${selected===c.id}" class="${selected===c.id?'selected':''}" onclick="saveTimedAnswer(${q.id},${c.id})">${esc(c.choice_text)}</button>`).join('')}</div>
    <button ${timedBusy?'disabled':''} aria-pressed="${timedExam.flagged.includes(q.id)}" onclick="flagTimedQuestion(${q.id})">${timedExam.flagged.includes(q.id)?'Remove review flag':'Flag for review'}</button>
    <button ${timedBusy||timedIndex===0?'disabled':''} onclick="timedIndex--;renderTimedExam()">Previous</button>
    <button ${timedBusy||timedIndex===timedExam.questions.length-1?'disabled':''} onclick="timedIndex++;renderTimedExam()">Next</button>
    <button ${timedBusy?'disabled':''} onclick="reviewTimedSubmission()">Finish session</button>
    <p id="timedSaveStatus" role="status">${timedBusy?'Saving…':'All displayed answers saved'}</p>
    <div id="timedFinishReview"></div><p id="timedError" role="alert"></p></div></div>`;
  tickTimedExam();
}
function reviewTimedSubmission(){
  const unanswered=timedExam.total_questions-Object.keys(timedExam.answers).length;
  document.getElementById('timedFinishReview').innerHTML=`<p>${unanswered} unanswered; ${timedExam.flagged.length} flagged for review. Submitting ends this session.</p><button class="primary" onclick="persistTimedExam({},timedExam.flagged,true)">Submit final answers</button>`;
}
async function saveTimedAnswer(questionId,choiceId){await persistTimedExam({[questionId]:choiceId},timedExam.flagged)}
async function flagTimedQuestion(questionId){
  const flags=timedExam.flagged.includes(questionId)?timedExam.flagged.filter(id=>id!==questionId):[...timedExam.flagged,questionId];
  await persistTimedExam({},flags);
}
async function persistTimedExam(answers,flagged,finish=false){
  if(timedBusy)return;
  timedBusy=true;renderTimedExam();
  try{
    timedExam=await api(`/api/exams/${timedExam.id}/${finish?'submit':'answers'}`,{method:finish?'POST':'PUT',body:JSON.stringify({revision:timedExam.revision,answers,flagged})});
    timedOffset=Date.parse(timedExam.server_now)-Date.now();
    timedBusy=false;renderTimedExam();
  }catch(e){
    timedBusy=false;renderTimedExam();
    document.getElementById('timedSaveStatus').textContent='Last change was not confirmed. Reload saved answers before continuing.';
    document.getElementById('timedError').innerHTML=`${esc(e.message)} <button onclick="reloadTimedExam()">Reload saved answers</button>`;
  }
}
async function reloadTimedExam(){
  try{timedExam=await api('/api/exams/'+timedExam.id);openTimedExam()}
  catch(e){const error=document.getElementById('timedError');if(error)error.textContent=e.message}
}
function tickTimedExam(){
  const timer=document.getElementById('examTimer');
  if(!timer){clearInterval(timedClock);return}
  const seconds=Math.max(0,Math.ceil((Date.parse(timedExam.deadline_at)-Date.now()-timedOffset)/1000));
  timer.textContent=`${Math.floor(seconds/60)}:${String(seconds%60).padStart(2,'0')}`;
  if(seconds===0&&!timedBusy){clearInterval(timedClock);reloadTimedExam()}
}
