from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.dependencies import get_db
from dtos import HotelDTO, HotelCreateDTO, HotelUpdateDTO
from services.mapper.Hotel import hotel_service

router = APIRouter(prefix="/hotels", tags=["Hotels"])


@router.get("/", response_model=list[HotelDTO])
def get_all_hotels(db: Session = Depends(get_db)):
    return hotel_service.get_all(db)


@router.get("/city")
def by_address(address: str, db: Session = Depends(get_db)):
    return hotel_service.get_by_address(db, address)


@router.get("/kosher")
def kosher_hotels(db: Session = Depends(get_db)):
    return hotel_service.get_kosher_hotels(db)


@router.get("/available-rooms")
def available_hotels(db: Session = Depends(get_db)):
    return hotel_service.hotels_with_available_rooms(db)


@router.get("/{hotel_id}", response_model=HotelDTO)
def get_hotel_by_id(hotel_id: int, db: Session = Depends(get_db)):
    return hotel_service.get_by_id(db, hotel_id)


@router.post("/", response_model=HotelDTO)
def create_hotel(payload: HotelCreateDTO, db: Session = Depends(get_db)):
    return hotel_service.create(db, payload)


@router.put("/{hotel_id}", response_model=HotelDTO)
def update_hotel(hotel_id: int, payload: HotelUpdateDTO, db: Session = Depends(get_db)):
    return hotel_service.update(db, hotel_id, payload)


@router.delete("/{hotel_id}")
def delete_hotel(hotel_id: int, db: Session = Depends(get_db)):
    return hotel_service.delete(db, hotel_id)
