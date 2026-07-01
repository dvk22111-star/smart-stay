from sqlalchemy.orm import Session
from models import CustomerPreferences


class CustomerPreferencesRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(CustomerPreferences).order_by(CustomerPreferences.CustomerPreferencesID).all()

    def get_by_id(self, pref_id: int):
        return self.db.query(CustomerPreferences).filter(CustomerPreferences.CustomerPreferencesID == pref_id).first()

    def get_by_user_id(self, user_id: int):
        return self.db.query(CustomerPreferences).filter(CustomerPreferences.UserID == user_id).all()

    def get_by_vacation_id(self, vacation_id: int):
        return self.db.query(CustomerPreferences).filter(CustomerPreferences.VacationID == vacation_id).all()

    def get_by_preference_id(self, preference_id: int):
        return self.db.query(CustomerPreferences).filter(CustomerPreferences.PreferencesID == preference_id).all()

    def get_by_user_vacation_preference(self, user_id: int, vacation_id: int, preference_id: int):
        return self.db.query(CustomerPreferences).filter(
            CustomerPreferences.UserID == user_id,
            CustomerPreferences.VacationID == vacation_id,
            CustomerPreferences.PreferencesID == preference_id,
        ).first()

    def create(self, item: CustomerPreferences):
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def update(self, item: CustomerPreferences):
        self.db.commit()
        self.db.refresh(item)
        return item

    def delete(self, item: CustomerPreferences):
        self.db.delete(item)
        self.db.commit()
        return True
