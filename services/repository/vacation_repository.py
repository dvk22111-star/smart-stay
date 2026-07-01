from datetime import date
from sqlalchemy.orm import Session
from models import Vacation


class VacationRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Vacation).order_by(Vacation.VacationID).all()

    def get_by_id(self, vacation_id: int):
        return self.db.query(Vacation).filter(Vacation.VacationID == vacation_id).first()

    def get_by_hotel_id(self, hotel_id: int):
        return self.db.query(Vacation).filter(Vacation.HotelID == hotel_id).order_by(Vacation.StartV).all()

    def get_active(self):
        today = date.today()
        return self.db.query(Vacation).filter(Vacation.StartV <= today, Vacation.EndV >= today).all()

    def get_future(self):
        today = date.today()
        return self.db.query(Vacation).filter(Vacation.StartV > today).all()

    def create(self, vacation: Vacation):
        self.db.add(vacation)
        self.db.commit()
        self.db.refresh(vacation)
        return vacation

    def update(self, vacation: Vacation):
        self.db.commit()
        self.db.refresh(vacation)
        return vacation

    def delete(self, vacation: Vacation):
        self.db.delete(vacation)
        self.db.commit()
        return True
