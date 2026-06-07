#!/usr/bin/env python3
"""Remove questions whose distractors are meta-instructions rather than real insurance answers."""
import sqlite3
import sys
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "pc_prep_v2.db"

BAD_PATTERNS = [
    "Ignore",
    "Treat it as",
    "Assume the loss",
    "broadest sounding",
    "fact pattern",
]


def main() -> None:
    if not DB_PATH.exists():
        print(f"DB not found at {DB_PATH}", file=sys.stderr)
        sys.exit(1)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Find question IDs that have at least one bad choice
    placeholders = " OR ".join(f"choice_text LIKE ?" for _ in BAD_PATTERNS)
    params = [f"%{p}%" for p in BAD_PATTERNS]
    cur.execute(
        f"SELECT DISTINCT question_id FROM answer_choices WHERE {placeholders}",
        params,
    )
    bad_qids = [row["question_id"] for row in cur.fetchall()]

    if not bad_qids:
        print("No bad questions found.")
        conn.close()
        return

    qid_placeholders = ",".join("?" for _ in bad_qids)

    # Delete child rows first (answer choices, quiz answers referencing these questions)
    cur.execute(f"DELETE FROM answer_choices WHERE question_id IN ({qid_placeholders})", bad_qids)
    choices_deleted = cur.rowcount

    cur.execute(f"DELETE FROM quiz_answers WHERE question_id IN ({qid_placeholders})", bad_qids)
    quiz_answers_deleted = cur.rowcount

    cur.execute(f"DELETE FROM mistake_bank WHERE question_id IN ({qid_placeholders})", bad_qids)

    cur.execute(f"DELETE FROM questions WHERE id IN ({qid_placeholders})", bad_qids)
    questions_deleted = cur.rowcount

    conn.commit()

    # Report remaining question count
    cur.execute("SELECT COUNT(*) FROM questions")
    remaining = cur.fetchone()[0]

    conn.close()

    print(f"Deleted {questions_deleted} bad questions ({choices_deleted} choices, {quiz_answers_deleted} quiz_answers).")
    print(f"Remaining questions in DB: {remaining}")


if __name__ == "__main__":
    main()
