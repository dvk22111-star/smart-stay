from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.dependencies import get_db
from assignment.assignment_engine import AssignmentEngine
from services.mapper.Placements import placement_service

router = APIRouter(prefix="/assignments", tags=["Assignments"])


@router.post("/run")
def run_assignment(payload: dict, db: Session = Depends(get_db)):
    """הפעלת מנוע השיבוץ עבור `vacation_id` (אופציונלי `hotel_id`)."""
    vacation_id = payload.get("vacation_id")
    hotel_id = payload.get("hotel_id")

    if vacation_id is None:
        raise HTTPException(status_code=400, detail="vacation_id is required")

    try:
        engine = AssignmentEngine(db)
        result = engine.run(vacation_id=vacation_id, hotel_id=hotel_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{vacation_id}")
def get_assignment(vacation_id: int, db: Session = Depends(get_db)):
    """החזרת רשימת השיבוצים עבור `vacation_id`."""
    placements = placement_service.get_by_vacation(db, vacation_id)
    return {"placements": placements}


@router.get("/{vacation_id}/report")
def get_assignment_report(vacation_id: int, db: Session = Depends(get_db)):
    """החזרת דוח שיבוץ ונתיבי קבצי Excel עבור הנופש."""
    try:
        engine = AssignmentEngine(db)
        report = engine.run(vacation_id=vacation_id)
        excel_export = report.get("excel_export") if isinstance(report, dict) else None
        return {
            "vacation_id": vacation_id,
            "excel_export": excel_export,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
