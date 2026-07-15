from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
import os
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


@router.get("/{vacation_id}/report/json")
def get_assignment_report_json(vacation_id: int, db: Session = Depends(get_db)):
    """החזרת דוח שיבוץ כ־JSON (טבלאות) עבור שימוש ב־UI/React.

    הפונקציה מריצה את מנוע השיבוץ (כמו `POST /assignments/run`) ומחזירה
    את טבלאות הדוח שנוצרו (למשל `empty_rooms`, `free_beds`, `low_score_women`).
    """
    try:
        engine = AssignmentEngine(db)
        report = engine.run(vacation_id=vacation_id)
        excel_export = report.get("excel_export") if isinstance(report, dict) else None
        tables = None
        if excel_export and isinstance(excel_export, dict):
            tables = excel_export.get("tables") or excel_export.get("tables", {})

        return {
            "vacation_id": vacation_id,
            "tables": tables,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{vacation_id}/report/empty_rooms")
def get_empty_rooms(vacation_id: int, db: Session = Depends(get_db)):
    """החזרת רשימת החדרים הריקים כ־JSON."""
    try:
        engine = AssignmentEngine(db)
        report = engine.run(vacation_id=vacation_id)
        excel_export = report.get("excel_export") if isinstance(report, dict) else None
        tables = excel_export.get("tables") if excel_export else {}
        return {"vacation_id": vacation_id, "empty_rooms": tables.get("empty_rooms", [])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{vacation_id}/report/low_score")
def get_low_score(vacation_id: int, db: Session = Depends(get_db)):
    """החזרת רשימת המשתתפים עם התאמה נמוכה (low score) כ־JSON."""
    try:
        engine = AssignmentEngine(db)
        report = engine.run(vacation_id=vacation_id)
        excel_export = report.get("excel_export") if isinstance(report, dict) else None
        tables = excel_export.get("tables") if excel_export else {}
        return {"vacation_id": vacation_id, "low_score": tables.get("low_score_women", [])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{vacation_id}/report/free_beds")
def get_free_beds(vacation_id: int, db: Session = Depends(get_db)):
    """החזרת רשימת המיטות החופשיות לפי חדר כ־JSON."""
    try:
        engine = AssignmentEngine(db)
        report = engine.run(vacation_id=vacation_id)
        excel_export = report.get("excel_export") if isinstance(report, dict) else None
        tables = excel_export.get("tables") if excel_export else {}
        return {"vacation_id": vacation_id, "free_beds": tables.get("free_beds", [])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{vacation_id}/export/{file_key}")
def download_excel(vacation_id: int, file_key: str, db: Session = Depends(get_db)):
    """הורדת קובץ Excel שנוצר עבור הנופש.

    `file_key` יכול להיות אחד מהבאים: `assignments`, `empty_rooms`, `free_beds`,
    `missing_women`, `low_score_women`.
    """
    allowed = {"assignments", "empty_rooms", "free_beds", "missing_women", "low_score_women"}
    if file_key not in allowed:
        raise HTTPException(status_code=400, detail=f"Invalid file_key, must be one of: {', '.join(sorted(allowed))}")

    try:
        engine = AssignmentEngine(db)
        report = engine.run(vacation_id=vacation_id)
        excel_export = report.get("excel_export") if isinstance(report, dict) else None
        paths = excel_export.get("paths", {}) if excel_export else {}
        path = paths.get(file_key)

        if not path or not os.path.exists(path):
            raise HTTPException(status_code=404, detail="Excel file not found for the requested key")

        return FileResponse(path, filename=os.path.basename(path), media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
