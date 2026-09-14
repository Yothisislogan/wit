"""Validate with --check (default); import atomically with --apply."""
import argparse
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app.content_loader import build_catalog, load_course, validate_catalog
from app.database import SessionLocal, create_all


def apply_content():
    data = build_catalog()
    validate_catalog(data)
    create_all()
    with SessionLocal() as db:
        try:
            load_course(db, data)
        except Exception:
            db.rollback()
            raise
    print("Content synchronized; existing IDs and student history preserved.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--check", action="store_true")
    group.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    if args.apply:
        apply_content()
    else:
        data = build_catalog()
        validate_catalog(data)
        for course in ("pc", "lh"):
            rows = [m for m in data["modules"] if m.get("course", "pc") == course]
            print(course, {"modules": len(rows), "lessons": sum(len(m.get("lessons", [])) for m in rows),
                           "questions": sum(len(m.get("questions", [])) for m in rows)})
        print("Validation passed. State-law generators excluded pending source review.")
