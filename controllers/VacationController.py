from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.dependencies import get_db
from dtos import VacationDTO, VacationCreateDTO, VacationUpdateDTO
from services.mapper.Vacation import vacation_service

router = APIRouter(prefix="/vacations", tags=["Vacations"])


@router.get("/", response_model=list[VacationDTO])
def get_all_vacations(db: Session = Depends(get_db)):
    return vacation_service.get_all_vacations(db)


@router.get("/active", response_model=list[VacationDTO])
def get_active_vacations(db: Session = Depends(get_db)):
    return vacation_service.get_active_vacations(db)


@router.get("/future", response_model=list[VacationDTO])
def get_future_vacations(db: Session = Depends(get_db)):
    return vacation_service.get_future_vacations(db)


@router.get("/hotel/{hotel_id}", response_model=list[VacationDTO])
def get_vacations_by_hotel(hotel_id: int, db: Session = Depends(get_db)):
    return vacation_service.get_vacations_by_hotel(db, hotel_id)


@router.get("/{vacation_id}", response_model=VacationDTO)
def get_vacation_by_id(vacation_id: int, db: Session = Depends(get_db)):
    return vacation_service.get_by_id(db, vacation_id)


@router.post("/", response_model=VacationDTO)
def create_vacation(payload: VacationCreateDTO, db: Session = Depends(get_db)):
    return vacation_service.create_vacation(db, payload)


@router.put("/{vacation_id}", response_model=VacationDTO)
def update_vacation(
    vacation_id: int,
    payload: VacationUpdateDTO,
    db: Session = Depends(get_db),
):
    return vacation_service.update_vacation(db, vacation_id, payload)


@router.delete("/{vacation_id}")
def delete_vacation(vacation_id: int, db: Session = Depends(get_db)):
    return vacation_service.delete_vacation(db, vacation_id)
