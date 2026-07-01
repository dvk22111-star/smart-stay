from fastapi import HTTPException
from sqlalchemy.orm import Session

from models import RoomPreferences
from services.repository.room_preferences_repository import RoomPreferencesRepository


class RoomPreferencesService:
    def get_all(self, db: Session):
        return RoomPreferencesRepository(db).get_all()

    def get_by_id(self, db: Session, room_pref_id: int):
        item = RoomPreferencesRepository(db).get_by_id(room_pref_id)
        if not item:
            raise HTTPException(status_code=404, detail="Room preference not found")
        return item

    def by_room(self, db: Session, room_id: int):
        return RoomPreferencesRepository(db).get_by_room_id(room_id)

    def by_preference(self, db: Session, preference_id: int):
        return RoomPreferencesRepository(db).get_by_preference_id(preference_id)

    def create(self, db: Session, payload):
        item = RoomPreferences(
            RoomID=payload.RoomID,
            IDPreferences=payload.IDPreferences,
        )
        return RoomPreferencesRepository(db).create(item)

    def update(self, db: Session, room_pref_id: int, payload):
        repo = RoomPreferencesRepository(db)
        item = repo.get_by_id(room_pref_id)
        if not item:
            raise HTTPException(status_code=404, detail="Room preference not found")
        if payload.RoomID is not None:
            item.RoomID = payload.RoomID
        if payload.IDPreferences is not None:
            item.IDPreferences = payload.IDPreferences
        return repo.update(item)

    def delete(self, db: Session, room_pref_id: int):
        repo = RoomPreferencesRepository(db)
        item = repo.get_by_id(room_pref_id)
        if not item:
            raise HTTPException(status_code=404, detail="Room preference not found")
        repo.delete(item)
        return {"deleted": True}


rp_service = RoomPreferencesService()
