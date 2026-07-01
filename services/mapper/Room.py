from fastapi import HTTPException
from sqlalchemy.orm import Session

from models import Room
from services.repository.room_repository import RoomRepository


class RoomService:
    def get_all(self, db: Session):
        return RoomRepository(db).get_all()

    def get_by_id(self, db: Session, room_id: int):
        room = RoomRepository(db).get_by_id(room_id)
        if not room:
            raise HTTPException(status_code=404, detail="Room not found")
        return room

    def by_hotel(self, db: Session, hotel_id: int):
        return RoomRepository(db).get_by_hotel_id(hotel_id)

    def by_beds(self, db: Session, beds: int):
        return RoomRepository(db).get_by_beds(beds)

    def by_floor(self, db: Session, floor: int):
        return RoomRepository(db).get_by_floor(floor)

    def create(self, db: Session, payload):
        room = Room(
            RoomNumber=payload.RoomNumber,
            Floor=payload.Floor,
            HotelID=payload.HotelID,
            NumberOfBeds=payload.NumberOfBeds,
        )
        return RoomRepository(db).create(room)

    def update(self, db: Session, room_id: int, payload):
        repo = RoomRepository(db)
        room = repo.get_by_id(room_id)
        if not room:
            raise HTTPException(status_code=404, detail="Room not found")
        if payload.RoomNumber is not None:
            room.RoomNumber = payload.RoomNumber
        if payload.Floor is not None:
            room.Floor = payload.Floor
        if payload.HotelID is not None:
            room.HotelID = payload.HotelID
        if payload.NumberOfBeds is not None:
            room.NumberOfBeds = payload.NumberOfBeds
        return repo.update(room)

    def delete(self, db: Session, room_id: int):
        repo = RoomRepository(db)
        room = repo.get_by_id(room_id)
        if not room:
            raise HTTPException(status_code=404, detail="Room not found")
        repo.delete(room)
        return {"deleted": True}


room_service = RoomService()
