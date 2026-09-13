"""Regression tests for student selection, grading, and saved study work.

Run: python -m unittest discover -s tests -v
All tests use a separate in-memory database; no content loaders or live AI run.
"""

import os
import unittest
from unittest.mock import patch

os.environ["DATABASE_URL"] = "sqlite://"

from fastapi.testclient import TestClient
from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app
from app.models import (
    AnswerChoice, Lesson, LessonProgress, MistakeBank, Module, Question,
    QuizAnswer, QuizAttempt, Term, User,
)
from app.tutor import _fallback_answer, get_tutor_context


class StudyFlowTests(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
        Base.metadata.create_all(self.engine)
        self.sessions = sessionmaker(bind=self.engine, expire_on_commit=False)

        def test_db():
            with self.sessions() as db:
                try:
                    yield db
                    db.commit()
                except Exception:
                    db.rollback()
                    raise

        app.dependency_overrides[get_db] = test_db
        # Do not enter app lifespan: it seeds the application database.
        self.client = TestClient(app)
        self.headers = {"X-Anon-Id": "test-student"}
        self.modules = {}
        self.lessons = {}
        self.questions = {}
        self.choices = {}
        with self.sessions() as db:
            user = User(anon_id="test-student", course="pc", state="AZ", name="Student")
            db.add(user)
            db.flush()
            self.user_id = user.id
            for slug, course in [
                ("pc-basics", "pc"), ("lh-basics", "lh"),
                ("state-law-az-pc", "pc"), ("state-law-ca-pc", "pc"),
                ("state-law-az-lh", "lh"), ("state-law-ca-lh", "lh"),
                ("inactive-pc", "pc"),
            ]:
                m = Module(slug=slug, title=slug, course=course, is_active=slug != "inactive-pc")
                db.add(m)
                db.flush()
                lesson = Lesson(module_id=m.id, slug=slug + "-lesson", title=slug, body="Coverage example")
                q = Question(module_id=m.id, question_text=slug + " question", explanation=slug + " explanation")
                db.add_all([lesson, q])
                db.flush()
                db.add(Term(module_id=m.id, lesson_id=lesson.id, term=slug + " term", exam_definition="Coverage example"))
                choices = [
                    AnswerChoice(question_id=q.id, choice_text=slug + " right", is_correct=True, sort_order=0, explanation="Right because " + slug),
                    AnswerChoice(question_id=q.id, choice_text=slug + " wrong", is_correct=False, sort_order=1, explanation="Wrong because " + slug),
                ]
                db.add_all(choices)
                db.flush()
                self.modules[slug], self.lessons[slug], self.questions[slug] = m.id, lesson.id, q.id
                self.choices[slug] = [c.id for c in choices]
            db.commit()

    def tearDown(self):
        self.client.close()
        app.dependency_overrides.clear()
        self.engine.dispose()

    def get(self, path):
        return self.client.get(path, headers=self.headers)

    def post(self, path, body):
        return self.client.post(path, headers=self.headers, json=body)

    def answer(self, slug, correct):
        return self.post("/api/quiz/submit", {"answers": {str(self.questions[slug]): self.choices[slug][0 if correct else 1]}})

    def test_anonymous_course_and_state_selection(self):
        self.assertEqual({m["slug"] for m in self.get("/api/modules").json()}, {"pc-basics", "state-law-az-pc"})
        self.post("/api/me/course", {"course": "lh"}).raise_for_status()
        self.post("/api/me/state", {"state": "CA"}).raise_for_status()
        self.assertEqual({m["slug"] for m in self.get("/api/modules").json()}, {"lh-basics", "state-law-ca-lh"})
        for endpoint in ["/api/questions?limit=50", "/api/terms"]:
            self.assertEqual({r["module_id"] for r in self.get(endpoint).json()}, {self.modules["lh-basics"], self.modules["state-law-ca-lh"]})

    def test_no_state_means_general_content_only(self):
        with self.sessions() as db:
            db.get(User, self.user_id).state = None
            db.commit()
        self.assertEqual([m["slug"] for m in self.get("/api/modules").json()], ["pc-basics"])

    def test_direct_links_and_studio_respect_selection(self):
        for slug in ["lh-basics", "state-law-ca-pc", "inactive-pc"]:
            self.assertEqual(self.get("/api/modules/" + slug).status_code, 404)
            self.assertEqual(self.get("/api/lessons/" + slug + "-lesson").status_code, 404)
            self.assertEqual(self.post("/api/studio/generate", {"action": "cram_sheet", "module_slug": slug}).status_code, 404)
            self.assertEqual(self.post(f"/api/lessons/{self.lessons[slug]}/progress", {"completed": True}).status_code, 404)
        self.assertEqual(self.get("/api/questions?module_slug=lh-basics").json(), [])
        self.assertEqual(self.get("/api/terms?module_slug=lh-basics").json(), [])
        self.assertEqual(self.get("/api/modules?course=invalid").status_code, 422)

    def test_choices_shuffle_without_changing_grading_or_leaking_answers(self):
        # Reverse rather than use probability, so a regression cannot pass by luck.
        with patch("app.main.random.shuffle", side_effect=lambda values: values.reverse()):
            question = self.get("/api/questions?module_slug=pc-basics").json()[0]
        self.assertEqual([c["id"] for c in question["choices"]], list(reversed(self.choices["pc-basics"])))
        self.assertEqual(question["explanation"], "")
        self.assertTrue(all("is_correct" not in c and c["explanation"] == "" for c in question["choices"]))
        result = self.answer("pc-basics", True).json()
        self.assertEqual(result["score"], 100)
        self.assertEqual(result["results"][0]["question"]["id"], question["id"])
        self.assertTrue(all(c["explanation"] for c in result["results"][0]["question"]["choices"]))

    def test_invalid_or_wrong_course_submission_rolls_back_entire_attempt(self):
        answers = {str(self.questions["pc-basics"]): self.choices["pc-basics"][0], str(self.questions["lh-basics"]): self.choices["lh-basics"][0]}
        self.assertEqual(self.post("/api/quiz/submit", {"answers": answers}).status_code, 400)
        self.assertEqual(self.post("/api/quiz/submit", {"answers": {}}).status_code, 400)
        self.assertEqual(self.post("/api/quiz/submit", {"answers": {str(self.questions["pc-basics"]): self.choices["state-law-az-pc"][0]}}).status_code, 400)
        with self.sessions() as db:
            self.assertEqual(db.scalar(select(func.count()).select_from(QuizAttempt)), 0)
            self.assertEqual(db.scalar(select(func.count()).select_from(QuizAnswer)), 0)

    def test_malformed_questions_are_not_served_or_graded(self):
        with self.sessions() as db:
            db.get(AnswerChoice, self.choices["pc-basics"][1]).is_correct = True
            db.commit()
        self.assertEqual(self.get("/api/questions?module_slug=pc-basics").json(), [])
        self.assertEqual(self.answer("pc-basics", True).status_code, 400)

    def test_partial_progress_saves_preserve_notes_confidence_and_bookmark(self):
        url = f"/api/lessons/{self.lessons['pc-basics']}/progress"
        self.post(url, {"notes": "A student's <saved> notes", "confidence": 3, "saved_for_review": True}).raise_for_status()
        saved = self.get("/api/lessons/pc-basics-lesson").json()["progress"]
        self.assertFalse(saved["completed"])
        self.post(url, {"completed": True}).raise_for_status()
        again = self.get("/api/lessons/pc-basics-lesson").json()["progress"]
        self.assertEqual({**saved, "completed": True}, again)
        self.post(url, {"notes": ""}).raise_for_status()
        final = self.get("/api/lessons/pc-basics-lesson").json()["progress"]
        self.assertEqual(final["notes"], "")
        self.assertTrue(final["completed"])
        self.assertTrue(final["saved_for_review"])

    def test_notes_survive_course_switches_and_are_private(self):
        self.post(f"/api/lessons/{self.lessons['pc-basics']}/progress", {"notes": "Keep this"}).raise_for_status()
        self.post("/api/me/course", {"course": "lh"})
        self.post("/api/me/course", {"course": "pc"})
        self.assertEqual(self.get("/api/lessons/pc-basics-lesson").json()["progress"]["notes"], "Keep this")
        other = self.client.get("/api/lessons/pc-basics-lesson", headers={"X-Anon-Id": "another-student"})
        self.assertEqual(other.json()["progress"]["notes"], "")

    def test_mistake_review_contains_only_active_misses_and_preserves_history(self):
        self.answer("pc-basics", False).raise_for_status()
        questions = self.get("/api/questions?mistakes_only=true").json()
        self.assertEqual([q["id"] for q in questions], [self.questions["pc-basics"]])
        self.answer("pc-basics", True).raise_for_status()
        self.assertEqual(self.get("/api/questions?mistakes_only=true").json(), [])
        self.assertEqual(self.get("/api/mistakes").json(), [])
        self.assertEqual(self.get("/api/dashboard").json()["mistakes"]["count"], 0)
        with self.sessions() as db:
            mistake = db.scalar(select(MistakeBank))
            self.assertIsNotNone(mistake.mastered_at)
        self.answer("pc-basics", False).raise_for_status()
        self.assertEqual(self.get("/api/mistakes").json()[0]["times_missed"], 2)

    def test_course_switch_excludes_old_progress_scores_and_mistakes(self):
        self.post(f"/api/lessons/{self.lessons['pc-basics']}/progress", {"completed": True})
        self.answer("pc-basics", False)
        self.post("/api/me/course", {"course": "lh"})
        d = self.get("/api/dashboard").json()
        self.assertEqual(d["lessons"]["completed"], 0)
        self.assertEqual(d["quizzes"]["total_taken"], 0)
        self.assertEqual(d["mistakes"]["count"], 0)
        self.assertEqual(self.get("/api/progress").json()["items"], [])
        self.assertEqual(self.get("/api/mistakes").json(), [])

    def test_old_mixed_quiz_scores_are_recalculated_for_selected_content(self):
        with self.sessions() as db:
            attempt = QuizAttempt(user_id=self.user_id, total_questions=2, score=50)
            db.add(attempt)
            db.flush()
            for slug, correct in [("pc-basics", True), ("lh-basics", False)]:
                db.add(QuizAnswer(attempt_id=attempt.id, question_id=self.questions[slug], selected_choice_id=self.choices[slug][0 if correct else 1], is_correct=correct))
            db.commit()
        pc = self.get("/api/dashboard").json()["quizzes"]
        self.assertEqual(pc["avg_score"], 100)
        self.assertEqual(pc["recent"][0]["total"], 1)
        self.post("/api/me/course", {"course": "lh"})
        self.assertEqual(self.get("/api/dashboard").json()["quizzes"]["avg_score"], 0)

    def test_dashboard_counts_all_attempts_but_limits_recent_history(self):
        for _ in range(12):
            self.answer("pc-basics", True).raise_for_status()
        quizzes = self.get("/api/dashboard").json()["quizzes"]
        self.assertEqual(quizzes["total_taken"], 12)
        self.assertEqual(len(quizzes["recent"]), 8)

    def test_coach_context_and_studio_terms_stay_in_selected_course_and_state(self):
        with self.sessions() as db:
            user = db.get(User, self.user_id)
            ctx = get_tutor_context(db, user, "coverage")
            allowed = {self.modules["pc-basics"], self.modules["state-law-az-pc"]}
            self.assertEqual({l.module_id for l in ctx.lessons}, allowed)
            self.assertEqual({t.module_id for t in ctx.terms}, allowed)
            user.course = "lh"
            lh_context = get_tutor_context(db, user, "coverage")
            fallback = _fallback_answer(lh_context, "Explain coinsurance", "lh")
            self.assertNotIn("insurance-to-value requirement", fallback["answer"])
            self.assertIn("lh-basics", fallback["answer"])
        result = self.post("/api/studio/generate", {"action": "cram_sheet", "module_slug": "pc-basics"}).json()
        self.assertEqual([t["term"] for t in result["terms"]], ["pc-basics term"])


if __name__ == "__main__":
    unittest.main()
