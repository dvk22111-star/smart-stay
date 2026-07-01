from sqlalchemy.orm import Session
from models import RoomPreferences


class RoomPreferencesRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(RoomPreferences).order_by(RoomPreferences.RoomPreferencesID).all()

    def get_by_id(self, room_pref_id: int):
        return self.db.query(RoomPreferences).filter(RoomPreferences.RoomPreferencesID == room_pref_id).first()

    def get_by_room_id(self, room_id: int):
        return self.db.query(RoomPreferences).filter(RoomPreferences.RoomID == room_id).all()

    def get_by_preference_id(self, preference_id: int):
        return self.db.query(RoomPreferences).filter(RoomPreferences.IDPreferences == preference_id).all()

    def create(self, item: RoomPreferences):
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def update(self, item: RoomPreferences):
        self.db.commit()
        self.db.refresh(item)
        return item

    def delete(self, item: RoomPreferences):
        self.db.delete(item)
        self.db.commit()
        return True
