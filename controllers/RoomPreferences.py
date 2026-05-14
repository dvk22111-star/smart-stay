
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from repositories.room_preferences_repository import RoomPreferencesRepository
from services.room_preferences_service import RoomPreferencesService
from models.room_preferences import Base

engine = create_engine("sqlite:///vacation.db")
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

Base.metadata.create_all(bind=engine)

room_pref_repo = RoomPreferencesRepository(session)
room_pref_service = RoomPreferencesService(room_pref_repo)

def create_room_preference_controller(room_id, preference_id):
    return room_pref_service.create_room_preference(room_id, preference_id)

def list_room_preferences_controller():
    return room_pref_service.get_all_room_preferences()
