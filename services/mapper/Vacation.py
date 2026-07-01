from fastapi import HTTPException
from sqlalchemy.orm import Session

from models import Vacation
from services.repository.vacation_repository import VacationRepository


class VacationService:
    def get_all_vacations(self, db: Session):
        return VacationRepository(db).get_all()

    def get_active_vacations(self, db: Session):
        return VacationRepository(db).get_active()

    def get_future_vacations(self, db: Session):
        return VacationRepository(db).get_future()

    def get_vacations_by_hotel(self, db: Session, hotel_id: int):
        return VacationRepository(db).get_by_hotel_id(hotel_id)

    def get_by_id(self, db: Session, vacation_id: int):
        vacation = VacationRepository(db).get_by_id(vacation_id)
        if not vacation:
            raise HTTPException(status_code=404, detail="Vacation not found")
        return vacation

    def create_vacation(self, db: Session, payload):
        vacation = Vacation(
            HotelID=payload.HotelID,
            StartV=payload.StartV,
            EndV=payload.EndV,
            Program=payload.Program,
            BasicCost=payload.BasicCost,
            NumberOfRooms=payload.NumberOfRooms,
            NumberOfFloors=payload.NumberOfFloors,
        )
        return VacationRepository(db).create(vacation)

    def update_vacation(self, db: Session, vacation_id: int, payload):
        repo = VacationRepository(db)
        vacation = repo.get_by_id(vacation_id)
        if not vacation:
            raise HTTPException(status_code=404, detail="Vacation not found")
        if payload.HotelID is not None:
            vacation.HotelID = payload.HotelID
        if payload.StartV is not None:
            vacation.StartV = payload.StartV
        if payload.EndV is not None:
            vacation.EndV = payload.EndV
        if payload.Program is not None:
            vacation.Program = payload.Program
        if payload.BasicCost is not None:
            vacation.BasicCost = payload.BasicCost
        if payload.NumberOfRooms is not None:
            vacation.NumberOfRooms = payload.NumberOfRooms
        if payload.NumberOfFloors is not None:
            vacation.NumberOfFloors = payload.NumberOfFloors
        return repo.update(vacation)

    def delete_vacation(self, db: Session, vacation_id: int):
        repo = VacationRepository(db)
        vacation = repo.get_by_id(vacation_id)
        if not vacation:
            raise HTTPException(status_code=404, detail="Vacation not found")
        repo.delete(vacation)
        return {"deleted": True}


vacation_service = VacationService()
