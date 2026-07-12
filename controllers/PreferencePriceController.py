from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.dependencies import get_db
from dtos import PreferencePriceDTO, PreferencePriceCreateDTO, PreferencePriceUpdateDTO
from services.mapper.PreferencePrice import preference_price_service

router = APIRouter(prefix="/preference-prices", tags=["PreferencePrices"])


@router.get("/", response_model=list[PreferencePriceDTO])
def get_all(db: Session = Depends(get_db)):
    return preference_price_service.get_all(db)


@router.get("/{id}", response_model=PreferencePriceDTO)
def get_by_id(id: int, db: Session = Depends(get_db)):
    return preference_price_service.get_by_id(db, id)


@router.get("/preference/{preference_id}", response_model=list[PreferencePriceDTO])
def get_by_preference(preference_id: int, db: Session = Depends(get_db)):
    return preference_price_service.by_preference(db, preference_id)


@router.post("/", response_model=PreferencePriceDTO)
def create(payload: PreferencePriceCreateDTO, db: Session = Depends(get_db)):
    return preference_price_service.create(db, payload)


@router.put("/{id}", response_model=PreferencePriceDTO)
def update(id: int, payload: PreferencePriceUpdateDTO, db: Session = Depends(get_db)):
    return preference_price_service.update(db, id, payload)


@router.delete("/{id}")
def delete(id: int, db: Session = Depends(get_db)):
    return preference_price_service.delete(db, id)
