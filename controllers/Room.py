

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from repositories.room_repository import RoomRepository
from services.room_service import RoomService
from models.room import Base

engine = create_engine("sqlite:///vacation.db")
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

Base.metadata.create_all(bind=engine)

room_repo = RoomRepository(session)
room_service = RoomService(room_repo)

def create_room_controller(room_number, floor, hotel_id, number_of_beds):
    return room_service.create_room(room_number, floor, hotel_id, number_of_beds)

def list_rooms_controller():
    return room_service.get_all_rooms()
