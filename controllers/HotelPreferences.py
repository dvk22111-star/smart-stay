
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from repositories.hotel_preferences_repository import HotelPreferencesRepository
from services.hotel_preferences_service import HotelPreferencesService
from models.hotel_preferences import Base

engine = create_engine("sqlite:///vacation.db")
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

Base.metadata.create_all(bind=engine)

hotel_pref_repo = HotelPreferencesRepository(session)
hotel_pref_service = HotelPreferencesService(hotel_pref_repo)

def create_hotel_preference_controller(hotel_id, preference_id, price):
    return hotel_pref_service.create_hotel_preference(hotel_id, preference_id, price)

def list_hotel_preferences_controller():
    return hotel_pref_service.get_all_hotel_preferences()
