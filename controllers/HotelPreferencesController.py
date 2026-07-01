from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.dependencies import get_db
from dtos import HotelPreferencesDTO, HotelPreferencesCreateDTO, HotelPreferencesUpdateDTO
from services.mapper.HotelPreferences import hp_service

router = APIRouter(prefix="/hotel-preferences", tags=["HotelPreferences"])


@router.get("/", response_model=list[HotelPreferencesDTO])
def get_all(db: Session = Depends(get_db)):
    return hp_service.get_all(db)


@router.get("/{id}", response_model=HotelPreferencesDTO)
def get_by_id(id: int, db: Session = Depends(get_db)):
    return hp_service.get_by_id(db, id)


@router.post("/", response_model=HotelPreferencesDTO)
def create(payload: HotelPreferencesCreateDTO, db: Session = Depends(get_db)):
    return hp_service.create(db, payload)


@router.put("/{id}", response_model=HotelPreferencesDTO)
def update(id: int, payload: HotelPreferencesUpdateDTO, db: Session = Depends(get_db)):
    return hp_service.update(db, id, payload)


@router.delete("/{id}")
def delete(id: int, db: Session = Depends(get_db)):
    return hp_service.delete(db, id)