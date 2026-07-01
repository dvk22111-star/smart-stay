from sqlalchemy.orm import Session
from models import HotelPreferences


class HotelPreferencesRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(HotelPreferences).order_by(HotelPreferences.HotelPreferencesID).all()

    def get_by_id(self, hotel_pref_id: int):
        return self.db.query(HotelPreferences).filter(HotelPreferences.HotelPreferencesID == hotel_pref_id).first()

    def get_by_hotel_id(self, hotel_id: int):
        return self.db.query(HotelPreferences).filter(HotelPreferences.HotelID == hotel_id).all()

    def get_by_preference_id(self, preference_id: int):
        return self.db.query(HotelPreferences).filter(HotelPreferences.PreferenceID == preference_id).all()

    def create(self, item: HotelPreferences):
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def update(self, item: HotelPreferences):
        self.db.commit()
        self.db.refresh(item)
        return item

    def delete(self, item: HotelPreferences):
        self.db.delete(item)
        self.db.commit()
        return True
