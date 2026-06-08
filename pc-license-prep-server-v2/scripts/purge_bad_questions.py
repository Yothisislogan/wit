#!/usr/bin/env python3
"""
purge_bad_questions.py — one-time cleanup of auto-generated template questions.

Auto-generated questions start with a bracket tag like:
  [BASELINE] Which of the following best describes...
  [SCENARIO] A policyholder...
  [EXCEPTION] All of the following are...

Real exam questions start with a capital letter (no leading bracket).

Run from pc-license-prep-server-v2/:
    python3 scripts/purge_bad_questions.py
"""
import sqlite3
import sys
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "pc_prep_v2.db"


def main() -> None:
    if not DB_PATH.exists():
        print(f"DB not found at {DB_PATH}", file=sys.stderr)
        sys.exit(1)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Count before
    cur.execute("SELECT COUNT(*) FROM questions")
    total_before = cur.fetchone()[0]
    print(f"Questions before purge: {total_before}")

    # Find auto-generated question IDs — all questions whose text starts with '['
    cur.execute("SELECT id FROM questions WHERE question_text LIKE '[%'")
    bad_qids = [row["id"] for row in cur.fetchall()]

    if not bad_qids:
        print("No auto-generated questions found. Nothing to delete.")
        cur.execute("SELECT COUNT(*) FROM questions")
        print(f"Questions remaining: {cur.fetchone()[0]}")
        conn.close()
        return

    qid_placeholders = ",".join("?" for _ in bad_qids)

    cur.execute(f"DELETE FROM answer_choices WHERE question_id IN ({qid_placeholders})", bad_qids)
    choices_deleted = cur.rowcount

    cur.execute(f"DELETE FROM quiz_answers WHERE question_id IN ({qid_placeholders})", bad_qids)
    quiz_answers_deleted = cur.rowcount

    cur.execute(f"DELETE FROM mistake_bank WHERE question_id IN ({qid_placeholders})", bad_qids)

    cur.execute(f"DELETE FROM questions WHERE id IN ({qid_placeholders})", bad_qids)
    questions_deleted = cur.rowcount

    conn.commit()

    cur.execute("SELECT COUNT(*) FROM questions")
    remaining = cur.fetchone()[0]

    conn.close()

    print(f"Deleted {questions_deleted} auto-generated questions "
          f"({choices_deleted} choices, {quiz_answers_deleted} quiz_answers).")
    print(f"Questions remaining: {remaining}")

    if remaining < 50:
        print("WARNING: fewer than 50 questions remain — you may want to re-run load_real_questions.py")
    elif remaining <= 100:
        print("✓ Count looks correct for the real exam question set (~70 expected).")
    else:
        print(f"NOTE: {remaining} questions remain — more than expected. "
              "Check for any non-bracket questions that were auto-generated.")


if __name__ == "__main__":
    main()
