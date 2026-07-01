from fastapi import HTTPException
from sqlalchemy.orm import Session

from models import PartnerRequest
from services.repository.partner_request_repository import PartnerRequestRepository


class PartnerRequestsService:
    def get_all(self, db: Session):
        return PartnerRequestRepository(db).get_all()

    def get_by_id(self, db: Session, request_id: int):
        item = PartnerRequestRepository(db).get_by_id(request_id)
        if not item:
            raise HTTPException(status_code=404, detail="Partner request not found")
        return item

    def by_user(self, db: Session, user_id: int):
        return PartnerRequestRepository(db).get_by_user_id(user_id)

    def by_vacation(self, db: Session, vacation_id: int):
        return PartnerRequestRepository(db).get_by_vacation_id(vacation_id)

    def create(self, db: Session, payload):
        item = PartnerRequest(
            UserIDMember1=payload.UserIDMember1,
            UserIDMember2=payload.UserIDMember2,
            VacationID=payload.VacationID,
        )
        return PartnerRequestRepository(db).create(item)

    def update(self, db: Session, request_id: int, payload):
        repo = PartnerRequestRepository(db)
        item = repo.get_by_id(request_id)
        if not item:
            raise HTTPException(status_code=404, detail="Partner request not found")
        if payload.UserIDMember1 is not None:
            item.UserIDMember1 = payload.UserIDMember1
        if payload.UserIDMember2 is not None:
            item.UserIDMember2 = payload.UserIDMember2
        if payload.VacationID is not None:
            item.VacationID = payload.VacationID
        return repo.update(item)

    def delete(self, db: Session, request_id: int):
        repo = PartnerRequestRepository(db)
        item = repo.get_by_id(request_id)
        if not item:
            raise HTTPException(status_code=404, detail="Partner request not found")
        repo.delete(item)
        return {"deleted": True}


pr_service = PartnerRequestsService()
