from sqlalchemy.orm import Session
from models import Placement, VacationersCustomers


class PlacementRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_room_id(self, room_id: int):
        return self.db.query(Placement).filter(Placement.RoomID == room_id).all()

    def get_by_vacation_id(self, vacation_id: int):
        return (
            self.db.query(Placement)
            .join(
                VacationersCustomers,
                Placement.VacationersCustomersID == VacationersCustomers.VacationIDForCustomers,
            )
            .filter(VacationersCustomers.VacationID == vacation_id)
            .all()
        )

    def get_available(self):
        return self.db.query(Placement).all()

    def get_by_id(self, placement_id: int):
        return self.db.query(Placement).filter(Placement.PlacementID == placement_id).first()

    def create(self, placement: Placement):
        self.db.add(placement)
        self.db.commit()
        self.db.refresh(placement)
        return placement

    def update(self, placement: Placement):
        self.db.commit()
        self.db.refresh(placement)
        return placement

    def delete(self, placement: Placement):
        self.db.delete(placement)
        self.db.commit()
        return True
