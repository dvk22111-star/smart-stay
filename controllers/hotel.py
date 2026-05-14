
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from repositories.hotel_repository import HotelRepository
from services.hotel_service import HotelService
from models.hotel import Base

engine = create_engine("sqlite:///vacation.db")
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

Base.metadata.create_all(bind=engine)

hotel_repo = HotelRepository(session)
hotel_service = HotelService(hotel_repo)

def create_hotel_controller(name, address, kosher=True, contact_person=""):
    return hotel_service.create_hotel(name, address, kosher, contact_person)

def list_hotels_controller():
    return hotel_service.get_all_hotels()
