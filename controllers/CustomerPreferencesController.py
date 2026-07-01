from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.dependencies import get_db
from dtos import CustomerPreferencesDTO, CustomerPreferencesCreateDTO, CustomerPreferencesUpdateDTO
from services.mapper.CustomerPreferences import cp_service

router = APIRouter(prefix="/customer-preferences", tags=["CustomerPreferences"])


@router.get("/", response_model=list[CustomerPreferencesDTO])
def get_all(db: Session = Depends(get_db)):
    return cp_service.get_all(db)


@router.get("/{id}", response_model=CustomerPreferencesDTO)
def get_by_id(id: int, db: Session = Depends(get_db)):
    return cp_service.get_by_id(db, id)


@router.post("/", response_model=CustomerPreferencesDTO)
def create(payload: CustomerPreferencesCreateDTO, db: Session = Depends(get_db)):
    return cp_service.create(db, payload)


@router.put("/{id}", response_model=CustomerPreferencesDTO)
def update(id: int, payload: CustomerPreferencesUpdateDTO, db: Session = Depends(get_db)):
    return cp_service.update(db, id, payload)


@router.delete("/{id}")
def delete(id: int, db: Session = Depends(get_db)):
    return cp_service.delete(db, id)