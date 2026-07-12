from fastapi import HTTPException
from sqlalchemy.orm import Session

from models import PreferencePrice
from services.repository.preference_price_repository import PreferencePriceRepository


class PreferencePriceService:
    def get_all(self, db: Session):
        return PreferencePriceRepository(db).get_all()

    def get_by_id(self, db: Session, preference_price_id: int):
        item = PreferencePriceRepository(db).get_by_id(preference_price_id)
        if not item:
            raise HTTPException(status_code=404, detail="Preference price not found")
        return item

    def by_preference(self, db: Session, preference_id: int):
        return PreferencePriceRepository(db).get_by_preference_id(preference_id)

    def create(self, db: Session, payload):
        item = PreferencePrice(
            PreferenceID=payload.PreferenceID,
            AdditionalPrice=payload.AdditionalPrice,
        )
        return PreferencePriceRepository(db).create(item)

    def update(self, db: Session, preference_price_id: int, payload):
        repo = PreferencePriceRepository(db)
        item = repo.get_by_id(preference_price_id)
        if not item:
            raise HTTPException(status_code=404, detail="Preference price not found")
        if payload.AdditionalPrice is not None:
            item.AdditionalPrice = payload.AdditionalPrice
        return repo.update(item)

    def delete(self, db: Session, preference_price_id: int):
        repo = PreferencePriceRepository(db)
        item = repo.get_by_id(preference_price_id)
        if not item:
            raise HTTPException(status_code=404, detail="Preference price not found")
        repo.delete(item)
        return {"deleted": True}


preference_price_service = PreferencePriceService()
