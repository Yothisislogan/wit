const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const source = fs.readFileSync(path.join(__dirname, '../frontend/app.js'), 'utf8').replace(/^boot\(\);$/m, '');

function harness() {
  const nodes = new Map();
  const makeNode = () => ({innerHTML: '', textContent: '', value: '', checked: false, disabled: false, focus() {}, classList: {add() {}, remove() {}}});
  nodes.set('app', makeNode());
  nodes.set('toast', makeNode());
  const context = vm.createContext({
    console,
    setTimeout() {},
    setInterval() {},
    clearInterval() {},
    document: {
      getElementById: id => nodes.get(id) || null,
      querySelector: () => ({focus() {}}),
      querySelectorAll: () => [],
    },
  });
  vm.runInContext(source, context);
  return {context, nodes, makeNode, app: nodes.get('app'), run: code => vm.runInContext(code, context)};
}

test('flashcard click handlers flip, move, and restart without lost local variables', async () => {
  const h = harness();
  h.context.api = async () => [
    {term: 'Peril', plain_english_definition: 'A cause of loss', exam_definition: 'Cause'},
    {term: 'Hazard', plain_english_definition: 'Increases risk', exam_definition: 'Risk'},
  ];
  await h.run('terms()');
  const handler = h.app.innerHTML.match(/class="flashcard"[^>]*onclick="([^"]+)"/)[1];
  h.run(handler);
  assert.match(h.app.innerHTML, /A cause of loss/);
  h.run(h.app.innerHTML.match(/onclick="(moveFlashcard\(1\))"/)[1]);
  assert.match(h.app.innerHTML, /Hazard/);
  h.run('flipFlashcard(); moveFlashcard(0)');
  assert.match(h.app.innerHTML, /Tap to reveal definition/);
});

test('review associates questions, chosen answers, and explanations by ID', () => {
  const h = harness();
  h.run(`currentQuestions=[
    {id:20,choices:[{id:202},{id:201}]},
    {id:10,choices:[{id:101},{id:102}]}
  ]; renderQuiz([
    {is_correct:true,selected_choice_id:101,question:{id:10,question_text:'Question ten',explanation:'Explanation ten',choices:[{id:101,choice_text:'Ten right',is_correct:true,explanation:'Ten rationale'},{id:102,choice_text:'Ten wrong'}]}},
    {is_correct:false,selected_choice_id:202,question:{id:20,question_text:'Question twenty',explanation:'Explanation twenty',choices:[{id:201,choice_text:'Twenty right',is_correct:true},{id:202,choice_text:'Twenty wrong',explanation:'Twenty rationale'}]}}
  ])`);
  const cards = h.app.innerHTML.split('style="border-left:4px solid').slice(1);
  assert.match(cards[0], /Question twenty[\s\S]*Twenty wrong[\s\S]*Your answer[\s\S]*Explanation twenty/);
  assert.doesNotMatch(cards[0], /Explanation ten/);
  assert.match(cards[1], /Question ten[\s\S]*Ten rationale[\s\S]*Explanation ten/);
});

test('reopening a lesson restores and escapes saved notes and review settings', async () => {
  const h = harness();
  h.context.api = async url => url.startsWith('/api/lessons/') ? {
    id:1, slug:'lesson', title:'Lesson', module_slug:'basics', module_title:'Basics', body:'Body',
    progress:{notes:'Saved <note> & details', confidence:3, saved_for_review:true},
  } : {lessons:[{slug:'lesson'}]};
  await h.run("showLesson('lesson')");
  assert.match(h.app.innerHTML, /Saved &lt;note&gt; &amp; details/);
  assert.match(h.app.innerHTML, /value="3" selected/);
  assert.match(h.app.innerHTML, /id="savedForReview" checked/);
});

test('saving notes omits completion and failed saves retain editable work', async () => {
  const h = harness();
  for (const id of ['notes','confidence','savedForReview','lessonSaveStatus']) h.nodes.set(id, h.makeNode());
  h.nodes.get('notes').value = 'Keep this note';
  h.nodes.get('confidence').value = '3';
  h.nodes.get('savedForReview').checked = true;
  let sent;
  h.context.api = async (url, opts) => {sent = JSON.parse(opts.body); return {ok:true};};
  await h.run('saveLessonNotes(1)');
  assert.equal(sent.notes, 'Keep this note');
  assert.equal(sent.saved_for_review, true);
  assert.equal('completed' in sent, false);
  h.context.api = async () => {throw Error('Offline');};
  assert.equal(await h.run('_saveLessonProgress(1,true)'), false);
  assert.equal(h.nodes.get('notes').value, 'Keep this note');
  assert.match(h.nodes.get('lessonSaveStatus').textContent, /Could not save/);
});

test('empty quiz and empty mistake queue display clear recovery screens', async () => {
  const h = harness();
  h.context.api = async () => [];
  await h.run("quiz('basics')");
  assert.match(h.app.innerHTML, /No practice questions are available/);
  await h.run('practiceMistakes()');
  assert.match(h.app.innerHTML, /no mistakes to review/);
});

test('new quiz preserves module selection and mistake review keeps its filter', async () => {
  const h = harness();
  const urls = [];
  h.context.api = async url => {urls.push(url); return [];};
  await h.run("quiz('basics');");
  await h.run('restartQuiz()');
  assert.equal(urls[0], urls[1]);
  assert.match(urls[1], /module_slug=basics/);
  await h.run('practiceMistakes()');
  await h.run('restartQuiz()');
  assert.match(urls[3], /mistakes_only=true/);
});

test('duplicate submit clicks send one request and failure preserves answers', async () => {
  const h = harness();
  h.run('currentQuestions=[{id:1,choices:[{id:11}]}]; answers={1:11};');
  let reject;
  let calls = 0;
  h.context.api = () => {calls++; return new Promise((resolve, fail) => {reject = fail;});};
  const first = h.run('submitQuiz()');
  await h.run('submitQuiz()');
  assert.equal(calls, 1);
  reject(Error('Offline'));
  await first;
  assert.equal(h.run('answers[1]'), 11);
  assert.equal(h.run('quizSubmitting'), false);
});

test('studio shuffle preserves the correct answer and rejects invalid generated quizzes', () => {
  const h = harness();
  const out = h.makeNode();
  h.context.out = out;
  h.run(`Math.random=()=>0; renderPracticeQuiz(out,{questions:[{q:'Question',choices:['Right','Wrong','Other'],correct:0}]})`);
  assert.notEqual(out._quizData[0].correct, 0);
  assert.equal(out._quizData[0].choices[out._quizData[0].correct], 'Right');
  h.run(`renderPracticeQuiz(out,{questions:[{q:'Invalid',choices:['A','B'],correct:9}]})`);
  assert.match(out.innerHTML, /studio-error/);
});

test('navigation catches asynchronous request failures', async () => {
  const h = harness();
  h.context.api = async () => {throw Error('Unavailable');};
  await h.run("route('lesson','missing')");
  assert.match(h.app.innerHTML, /Something went wrong/);
  assert.match(h.app.innerHTML, /Back to dashboard/);
});

test('state profiles distinguish separate exams and scaled scores from percentages', () => {
  const h=harness();
  assert.equal(h.run("examProfileSummary({profiles:[]},'pc')"),'Exam format awaiting verification');
  const summary=h.run(`examProfileSummary({reviewed_at:'2026-09-13',profiles:[{name:'Property',course:'pc',scored_questions:55,pretest_questions_max:5,duration_minutes:75,passing_score:70}]},'pc')`);
  assert.match(summary,/55 scored.*75 min.*scaled score 70/);
  assert.doesNotMatch(summary,/%/);
});

function examFixture(h){
  h.run(`timedExam={id:'exam-1',course:'pc',status:'in_progress',revision:0,server_now:new Date().toISOString(),deadline_at:new Date(Date.now()+60000).toISOString(),answers:{},flagged:[],total_questions:1,questions:[{id:42,question_text:'Question <safe>',choices:[{id:421,choice_text:'Option'}]}]}`);
  for(const id of ['examTimer','timedSaveStatus','timedError','timedFinishReview'])h.nodes.set(id,h.makeNode());
}

test('timed practice saves stable IDs and locks controls while saving', async () => {
  const h=harness();examFixture(h);
  let resolve;let calls=0;
  h.context.api=(url,opts)=>{calls++;assert.equal(url,'/api/exams/exam-1/answers');assert.deepEqual(JSON.parse(opts.body).answers,{'42':421});return new Promise(r=>resolve=r)};
  const pending=h.run('saveTimedAnswer(42,421)');
  assert.match(h.app.innerHTML,/Saving/);
  await h.run('saveTimedAnswer(42,421)');assert.equal(calls,1);
  const response=JSON.parse(h.run('JSON.stringify(timedExam)'));response.revision=1;response.answers={'42':421};resolve(response);
  await pending;
  assert.equal(h.run('timedExam.answers[42]'),421);
  assert.match(h.app.innerHTML,/aria-pressed="true"/);
  assert.match(h.app.innerHTML,/Question &lt;safe&gt;/);
});

test('failed timed save retains server-confirmed answers and offers reload', async () => {
  const h=harness();examFixture(h);
  h.context.api=async()=>{throw new Error('offline')};
  await h.run('saveTimedAnswer(42,421)');
  assert.equal(h.run('Object.keys(timedExam.answers).length'),0);
  assert.match(h.nodes.get('timedSaveStatus').textContent,/not confirmed/);
  assert.match(h.nodes.get('timedError').innerHTML,/Reload saved answers/);
});
