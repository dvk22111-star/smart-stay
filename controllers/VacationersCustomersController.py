from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.dependencies import get_db
from dtos import VacationersCustomersDTO, VacationersCustomersCreateDTO, VacationersCustomersUpdateDTO
from services.mapper.VacationersCustomers import vc_service# vacationers_customers_service

router = APIRouter(prefix="/vacationers-customers", tags=["VacationersCustomers"])


@router.get("/", response_model=list[VacationersCustomersDTO])
def get_all(db: Session = Depends(get_db)):
    return vc_service.get_all(db)


@router.get("/{id}", response_model=VacationersCustomersDTO)
def get_by_id(id: int, db: Session = Depends(get_db)):
    return vc_service.get_by_id(db, id)


@router.post("/", response_model=VacationersCustomersDTO)
def create(payload: VacationersCustomersCreateDTO, db: Session = Depends(get_db)):
    return vc_service.create(db, payload)


@router.put("/{id}", response_model=VacationersCustomersDTO)
def update(id: int, payload: VacationersCustomersUpdateDTO, db: Session = Depends(get_db)):
    return vc_service.update(db, id, payload)


@router.delete("/{id}")
def delete(id: int, db: Session = Depends(get_db)):
    return vc_service.delete(db, id)