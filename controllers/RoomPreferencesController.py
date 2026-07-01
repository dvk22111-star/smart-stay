from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.dependencies import get_db
from dtos import RoomPreferencesDTO, RoomPreferencesCreateDTO, RoomPreferencesUpdateDTO
from services.mapper.RoomPreferences import rp_service

router = APIRouter(prefix="/room-preferences", tags=["RoomPreferences"])


@router.get("/", response_model=list[RoomPreferencesDTO])
def get_all(db: Session = Depends(get_db)):
    return rp_service.get_all(db)


@router.get("/{id}", response_model=RoomPreferencesDTO)
def get_by_id(id: int, db: Session = Depends(get_db)):
    return rp_service.get_by_id(db, id)


@router.post("/", response_model=RoomPreferencesDTO)
def create(payload: RoomPreferencesCreateDTO, db: Session = Depends(get_db)):
    return rp_service.create(db, payload)


@router.put("/{id}", response_model=RoomPreferencesDTO)
def update(id: int, payload: RoomPreferencesUpdateDTO, db: Session = Depends(get_db)):
    return rp_service.update(db, id, payload)


@router.delete("/{id}")
def delete(id: int, db: Session = Depends(get_db)):
    return rp_service.delete(db, id)