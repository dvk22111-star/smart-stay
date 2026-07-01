from sqlalchemy.orm import Session
from models import Room


class RoomRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Room).order_by(Room.RoomID).all()

    def get_by_id(self, room_id: int):
        return self.db.query(Room).filter(Room.RoomID == room_id).first()

    def get_by_hotel_id(self, hotel_id: int):
        return self.db.query(Room).filter(Room.HotelID == hotel_id).order_by(Room.RoomNumber).all()

    def get_by_beds(self, beds: int):
        return self.db.query(Room).filter(Room.NumberOfBeds >= beds).all()

    def get_by_floor(self, floor: int):
        return self.db.query(Room).filter(Room.Floor == floor).all()

    def create(self, room: Room):
        self.db.add(room)
        self.db.commit()
        self.db.refresh(room)
        return room

    def update(self, room: Room):
        self.db.commit()
        self.db.refresh(room)
        return room

    def delete(self, room: Room):
        self.db.delete(room)
        self.db.commit()
        return True
