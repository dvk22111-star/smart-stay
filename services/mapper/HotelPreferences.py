from fastapi import HTTPException
from sqlalchemy.orm import Session

from models import HotelPreferences
from services.repository.hotel_preferences_repository import HotelPreferencesRepository


class HotelPreferencesService:
    def get_all(self, db: Session):
        return HotelPreferencesRepository(db).get_all()

    def get_by_id(self, db: Session, hotel_pref_id: int):
        item = HotelPreferencesRepository(db).get_by_id(hotel_pref_id)
        if not item:
            raise HTTPException(status_code=404, detail="Hotel preference not found")
        return item

    def by_hotel(self, db: Session, hotel_id: int):
        return HotelPreferencesRepository(db).get_by_hotel_id(hotel_id)

    def create(self, db: Session, payload):
        item = HotelPreferences(
            HotelID=payload.HotelID,
            PreferenceID=payload.PreferenceID,
            Price=payload.Price,
        )
        return HotelPreferencesRepository(db).create(item)

    def update(self, db: Session, hotel_pref_id: int, payload):
        repo = HotelPreferencesRepository(db)
        item = repo.get_by_id(hotel_pref_id)
        if not item:
            raise HTTPException(status_code=404, detail="Hotel preference not found")
        if payload.Price is not None:
            item.Price = payload.Price
        return repo.update(item)

    def delete(self, db: Session, hotel_pref_id: int):
        repo = HotelPreferencesRepository(db)
        item = repo.get_by_id(hotel_pref_id)
        if not item:
            raise HTTPException(status_code=404, detail="Hotel preference not found")
        repo.delete(item)
        return {"deleted": True}


hp_service = HotelPreferencesService()
