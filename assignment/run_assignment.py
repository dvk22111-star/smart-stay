import os
import sys

# ודא שספריית הפרויקט והספריה 'assignment' ב־sys.path
ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
ASSIGNMENT_DIR = os.path.dirname(__file__)
if ASSIGNMENT_DIR not in sys.path:
    sys.path.insert(0, ASSIGNMENT_DIR)

from database.connection import SessionLocal
from assignment.assignment_engine import AssignmentEngine


def run():
    session = SessionLocal()

    try:
        engine = AssignmentEngine(session)

        result = engine.run(vacation_id=1)

        placements = result.get("placements") if isinstance(result, dict) else result
        count = len(placements) if placements is not None else 0
        print(f"נוצרו {count} שיבוצים")

        if isinstance(result, dict):
            excel_export = result.get("excel_export")
            if excel_export:
                print("Excel export results:")
                for name, path in excel_export.get("paths", {}).items():
                    print(f"  {name}: {path}")
            else:
                print("No Excel export available.")

    finally:
        session.close()


if __name__ == "__main__":
    run()