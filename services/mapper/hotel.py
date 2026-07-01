from fastapi import HTTPException
from sqlalchemy.orm import Session

from models import Hotel
from services.repository.hotel_repository import HotelRepository


class HotelService:
    def get_all(self, db: Session):
        return HotelRepository(db).get_all()

    def get_by_id(self, db: Session, hotel_id: int):
        hotel = HotelRepository(db).get_by_id(hotel_id)
        if not hotel:
            raise HTTPException(status_code=404, detail="Hotel not found")
        return hotel

    def get_by_address(self, db: Session, address: str):
        return HotelRepository(db).get_by_address(address)

    def get_kosher_hotels(self, db: Session):
        return HotelRepository(db).get_kosher()

    def hotels_with_available_rooms(self, db: Session):
        return HotelRepository(db).get_all()

    def create(self, db: Session, payload):
        hotel = Hotel(
            Name=payload.Name,
            Address=payload.Address,
            Kosher=payload.Kosher,
            ContactPerson=payload.ContactPerson,
        )
        return HotelRepository(db).create(hotel)

    def update(self, db: Session, hotel_id: int, payload):
        repo = HotelRepository(db)
        hotel = repo.get_by_id(hotel_id)
        if not hotel:
            raise HTTPException(status_code=404, detail="Hotel not found")
        if payload.Name is not None:
            hotel.Name = payload.Name
        if payload.Address is not None:
            hotel.Address = payload.Address
        if payload.Kosher is not None:
            hotel.Kosher = payload.Kosher
        if payload.ContactPerson is not None:
            hotel.ContactPerson = payload.ContactPerson
        return repo.update(hotel)

    def delete(self, db: Session, hotel_id: int):
        repo = HotelRepository(db)
        hotel = repo.get_by_id(hotel_id)
        if not hotel:
            raise HTTPException(status_code=404, detail="Hotel not found")
        repo.delete(hotel)
        return {"deleted": True}


hotel_service = HotelService()
