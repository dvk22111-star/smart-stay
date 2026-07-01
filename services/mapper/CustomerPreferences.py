from fastapi import HTTPException
from sqlalchemy.orm import Session

from models import CustomerPreferences
from services.repository.customer_preferences_repository import CustomerPreferencesRepository


class CustomerPreferencesService:
    def get_all(self, db: Session):
        return CustomerPreferencesRepository(db).get_all()

    def get_by_id(self, db: Session, pref_id: int):
        item = CustomerPreferencesRepository(db).get_by_id(pref_id)
        if not item:
            raise HTTPException(status_code=404, detail="Customer preference not found")
        return item

    def get_by_user(self, db: Session, user_id: int):
        return CustomerPreferencesRepository(db).get_by_user_id(user_id)

    def get_by_vacation(self, db: Session, vacation_id: int):
        return CustomerPreferencesRepository(db).get_by_vacation_id(vacation_id)

    def get_by_preference(self, db: Session, preference_id: int):
        return CustomerPreferencesRepository(db).get_by_preference_id(preference_id)

    def create(self, db: Session, payload):
        item = CustomerPreferences(
            Rating=payload.Rating,
            UserID=payload.UserID,
            PreferencesID=payload.PreferencesID,
            VacationID=payload.VacationID,
        )
        return CustomerPreferencesRepository(db).create(item)

    def update(self, db: Session, pref_id: int, payload):
        repo = CustomerPreferencesRepository(db)
        item = repo.get_by_id(pref_id)
        if not item:
            raise HTTPException(status_code=404, detail="Customer preference not found")
        if payload.Rating is not None:
            item.Rating = payload.Rating
        return repo.update(item)

    def delete(self, db: Session, pref_id: int):
        repo = CustomerPreferencesRepository(db)
        item = repo.get_by_id(pref_id)
        if not item:
            raise HTTPException(status_code=404, detail="Customer preference not found")
        repo.delete(item)
        return {"deleted": True}


cp_service = CustomerPreferencesService()
