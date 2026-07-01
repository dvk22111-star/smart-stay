from sqlalchemy.orm import Session
from models import VacationersCustomers


class VacationersCustomersRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_vacation_id(self, vacation_id: int):
        return self.db.query(VacationersCustomers).filter(VacationersCustomers.VacationID == vacation_id).all()

    def get_by_user_id(self, user_id: int):
        return self.db.query(VacationersCustomers).filter(VacationersCustomers.UserID == user_id).all()

    def create(self, item: VacationersCustomers):
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def update(self, item: VacationersCustomers):
        self.db.commit()
        self.db.refresh(item)
        return item

    def delete(self, item: VacationersCustomers):
        self.db.delete(item)
        self.db.commit()
        return True
