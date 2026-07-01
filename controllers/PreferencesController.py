from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.dependencies import get_db
from dtos import PreferencesDTO, PreferencesCreateDTO#, PreferencesUpdateDTO
from services.mapper.Preferences import preferences_service

router = APIRouter(prefix="/preferences", tags=["Preferences"])


@router.get("/", response_model=list[PreferencesDTO])
def get_all(db: Session = Depends(get_db)):
    return preferences_service.get_all(db)


@router.get("/{id}", response_model=PreferencesDTO)
def get_by_id(id: int, db: Session = Depends(get_db)):
    return preferences_service.get_by_id(db, id)


@router.post("/", response_model=PreferencesDTO)
def create(payload: PreferencesCreateDTO, db: Session = Depends(get_db)):
    return preferences_service.create(db, payload)


#@router.put("/{id}", response_model=PreferencesDTO)
#def update(id: int, payload: PreferencesUpdateDTO, db: Session = Depends(get_db)):
#    return preferences_service.update(db, id, payload)


@router.delete("/{id}")
def delete(id: int, db: Session = Depends(get_db)):
    return preferences_service.delete(db, id)