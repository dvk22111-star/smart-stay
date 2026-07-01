from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.dependencies import get_db
from dtos import RoomDTO, RoomCreateDTO, RoomUpdateDTO
from services.mapper.Room import room_service

router = APIRouter(prefix="/rooms", tags=["Rooms"])


@router.get("/", response_model=list[RoomDTO])
def get_all_rooms(db: Session = Depends(get_db)):
    return room_service.get_all(db)


@router.get("/{room_id}", response_model=RoomDTO)
def get_room_by_id(room_id: int, db: Session = Depends(get_db)):
    return room_service.get_by_id(db, room_id)


@router.get("/hotel/{hotel_id}")
def by_hotel(hotel_id: int, db: Session = Depends(get_db)):
    return room_service.by_hotel(db, hotel_id)


@router.get("/beds/{beds}")
def by_beds(beds: int, db: Session = Depends(get_db)):
    return room_service.by_beds(db, beds)


@router.get("/floor/{floor}")
def by_floor(floor: int, db: Session = Depends(get_db)):
    return room_service.by_floor(db, floor)


@router.post("/", response_model=RoomDTO)
def create_room(payload: RoomCreateDTO, db: Session = Depends(get_db)):
    return room_service.create(db, payload)


@router.put("/{room_id}", response_model=RoomDTO)
def update_room(room_id: int, payload: RoomUpdateDTO, db: Session = Depends(get_db)):
    return room_service.update(db, room_id, payload)


@router.delete("/{room_id}")
def delete_room(room_id: int, db: Session = Depends(get_db)):
    return room_service.delete(db, room_id)
