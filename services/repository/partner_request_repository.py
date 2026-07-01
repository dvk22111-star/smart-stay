from sqlalchemy.orm import Session
from models import PartnerRequest


class PartnerRequestRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(PartnerRequest).order_by(PartnerRequest.PartnerRequestID).all()

    def get_by_id(self, request_id: int):
        return self.db.query(PartnerRequest).filter(PartnerRequest.PartnerRequestID == request_id).first()

    def get_by_user_id(self, user_id: int):
        return self.db.query(PartnerRequest).filter(
            (PartnerRequest.UserIDMember1 == user_id) | (PartnerRequest.UserIDMember2 == user_id)
        ).all()

    def get_by_vacation_id(self, vacation_id: int):
        return self.db.query(PartnerRequest).filter(PartnerRequest.VacationID == vacation_id).all()

    def create(self, item: PartnerRequest):
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def update(self, item: PartnerRequest):
        self.db.commit()
        self.db.refresh(item)
        return item

    def delete(self, item: PartnerRequest):
        self.db.delete(item)
        self.db.commit()
        return True
