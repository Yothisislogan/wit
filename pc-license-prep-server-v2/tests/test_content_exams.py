"""Content preservation and real server-enforced exam lifecycle regressions."""
import json
import unittest
from datetime import timedelta
from unittest.mock import patch

from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import sessionmaker
from app.content_loader import build_catalog, load_course
from app.database import Base
from app.models import AnswerChoice, Lesson, LessonProgress, Module, Question, QuizAnswer, QuizAttempt, TimedExam, User
from app.exams import utcnow
import test_study


class ContentTests(unittest.TestCase):
    def test_fresh_import_rerun_and_partial_repair_preserve_history(self):
        engine = create_engine('sqlite://')
        Base.metadata.create_all(engine)
        with sessionmaker(bind=engine)() as db:
            catalog = build_catalog()
            load_course(db, catalog)
            self.assertEqual(db.scalar(select(func.count(Lesson.id))), 123)
            self.assertEqual(db.scalar(select(func.count(Question.id))), 404)
            self.assertEqual(set(db.scalars(select(Module.course))), {'pc', 'lh'})
            question = db.scalar(select(Question).limit(1))
            qid, cid = question.id, question.choices[0].id
            question.is_active = False
            lesson = db.scalar(select(Lesson).limit(1))
            lesson.body = 'A custom instructor edit.'
            user = User(anon_id='preserve'); db.add(user); db.flush()
            progress = LessonProgress(user_id=user.id, lesson_id=lesson.id, notes='My saved notes', completed=True)
            attempt = QuizAttempt(user_id=user.id, score=1, total_questions=1)
            db.add_all([progress, attempt]); db.flush()
            db.add(QuizAnswer(attempt_id=attempt.id, question_id=qid, selected_choice_id=cid, is_correct=True))
            # Simulate an interrupted historical import missing the last module.
            missing = db.scalar(select(Module).where(Module.slug == catalog['modules'][-1]['slug']))
            db.delete(missing); db.commit()
            load_course(db, build_catalog())
            self.assertEqual(db.scalar(select(func.count(Question.id))), 404)
            self.assertFalse(db.get(Question, qid).is_active)
            self.assertEqual(db.get(AnswerChoice, cid).question_id, qid)
            self.assertEqual(lesson.body, 'A custom instructor edit.')
            self.assertEqual(progress.notes, 'My saved notes')
            self.assertTrue(progress.completed)
            self.assertEqual(db.scalar(select(QuizAnswer)).selected_choice_id, cid)
            counts = [db.scalar(select(func.count(model.id))) for model in (Module, Lesson, Question, AnswerChoice)]
            load_course(db, build_catalog())
            self.assertEqual(counts, [db.scalar(select(func.count(model.id))) for model in (Module, Lesson, Question, AnswerChoice)])
        engine.dispose()

    def test_invalid_catalog_fails_before_any_write(self):
        engine = create_engine('sqlite://')
        Base.metadata.create_all(engine)
        with sessionmaker(bind=engine)() as db:
            catalog = build_catalog()
            catalog['modules'][-1]['questions'].append(('Bad', 'multiple_choice', 'standard', 'Explanation', [('A', True, ''), ('B', True, '')]))
            with self.assertRaises(ValueError):
                load_course(db, catalog)
            self.assertEqual(db.scalar(select(func.count(Module.id))), 0)
        engine.dispose()


class TimedExamTests(unittest.TestCase):
    setUp = test_study.StudyFlowTests.setUp
    tearDown = test_study.StudyFlowTests.tearDown

    def populate(self):
        with self.sessions() as db:
            module = db.scalar(select(Module).where(Module.slug == 'pc-basics'))
            for i in range(55):
                q = Question(module_id=module.id, question_text=f'Unique exam question {i}', explanation=f'Reason {i}')
                db.add(q); db.flush()
                db.add_all([AnswerChoice(question_id=q.id, choice_text='Correct', is_correct=True), AnswerChoice(question_id=q.id, choice_text='Incorrect', is_correct=False)])
            db.commit()

    def start(self):
        self.populate()
        response = self.client.post('/api/exams', headers=self.headers)
        self.assertEqual(response.status_code, 200, response.text)
        return response.json()

    def test_insufficient_bank_is_explicit(self):
        result = self.client.post('/api/exams', headers=self.headers)
        self.assertEqual(result.status_code, 409)
        self.assertIn('50 unique valid questions', result.text)

    def test_snapshot_resume_privacy_and_atomic_save(self):
        exam = self.start()
        self.assertEqual(exam['total_questions'], 50)
        self.assertNotIn('is_correct', json.dumps(exam))
        self.assertNotIn('explanation', json.dumps(exam))
        self.assertFalse(any('state-law' in q['module_title'] for q in exam['questions']))
        q = exam['questions'][0]; choice = q['choices'][0]['id']
        saved = self.client.put(f"/api/exams/{exam['id']}/answers", headers=self.headers, json={'revision':0, 'answers':{q['id']:choice}, 'flagged':[q['id']]}).json()
        self.assertEqual(saved['answers'], {str(q['id']):choice})
        resumed = self.client.post('/api/exams', headers=self.headers).json()
        self.assertEqual(resumed['id'], exam['id'])
        self.assertEqual(resumed['questions'], exam['questions'])
        self.assertEqual(resumed['flagged'], [q['id']])
        stale = self.client.put(f"/api/exams/{exam['id']}/answers", headers=self.headers, json={'revision':0, 'answers':{}})
        self.assertEqual(stale.status_code,409)
        invalid = self.client.put(f"/api/exams/{exam['id']}/answers", headers=self.headers, json={'revision':1, 'answers':{q['id']:999999}})
        self.assertEqual(invalid.status_code,422)
        other = self.client.get(f"/api/exams/{exam['id']}",headers={'X-Anon-Id':'another-student'})
        self.assertEqual(other.status_code,404)
        with self.sessions() as db:
            db.get(Question,q['id']).question_text='Edited after starting'
            db.commit()
        self.assertEqual(self.client.get(f"/api/exams/{exam['id']}",headers=self.headers).json()['questions'],exam['questions'])

    def test_expiry_ignores_late_answers_and_submission_is_idempotent(self):
        exam = self.start()
        with self.sessions() as db:
            stored = db.get(TimedExam, exam['id'])
            snapshot = json.loads(stored.snapshot_json)
            right = {q['id']: next(c['id'] for c in q['choices'] if c['is_correct']) for q in snapshot}
        first_id = next(iter(right))
        self.client.put(f"/api/exams/{exam['id']}/answers",headers=self.headers,json={'revision':0,'answers':{first_id:right[first_id]}})
        with self.sessions() as db:
            db.get(TimedExam,exam['id']).deadline_at=utcnow()-timedelta(seconds=1)
            db.commit()
        late=self.client.post(f"/api/exams/{exam['id']}/submit",headers=self.headers,json={'revision':1,'answers':right})
        self.assertEqual(late.status_code,200,late.text)
        result=late.json()
        self.assertEqual(result['status'],'completed')
        self.assertEqual(result['result']['correct'],1)
        self.assertEqual(result['result']['percent'],2)
        retry=self.client.post(f"/api/exams/{exam['id']}/submit",headers=self.headers,json={'revision':0,'answers':right}).json()
        self.assertEqual(result['result'],retry['result'])
        self.assertEqual(self.client.get('/api/exams/active',headers=self.headers).json()['exam']['id'],exam['id'])
        next_exam=self.client.post('/api/exams',headers=self.headers).json()
        self.assertNotEqual(next_exam['id'],exam['id'])

    def test_submit_grades_all_answers_and_survives_course_switch(self):
        exam = self.start()
        with self.sessions() as db:
            snapshot=json.loads(db.get(TimedExam,exam['id']).snapshot_json)
            right={q['id']:next(c['id'] for c in q['choices'] if c['is_correct']) for q in snapshot}
            db.get(User,self.user_id).course='lh'; db.commit()
        response=self.client.post(f"/api/exams/{exam['id']}/submit",headers=self.headers,json={'revision':0,'answers':right})
        self.assertEqual(response.status_code,200,response.text)
        self.assertEqual(response.json()['course'],'pc')
        self.assertEqual(response.json()['result']['percent'],100)

    def test_profiles_never_invent_counts_or_percent_passing(self):
        nc=self.client.get('/api/state-info/NC').json()
        self.assertEqual(len(nc['profiles']),4)
        self.assertEqual(nc['profiles'][0]['scored_questions'],55)
        self.assertEqual(nc['profiles'][0]['score_type'],'scaled')
        az=self.client.get('/api/state-info/AZ').json()
        self.assertIsNone(az['pc_exam'])
        self.assertEqual(az['review_status'],'pending')
        self.assertEqual(az['profiles'],[])
