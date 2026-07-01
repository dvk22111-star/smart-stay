from fastapi import HTTPException
from sqlalchemy.orm import Session

from models import VacationersCustomers
from services.repository.vacationers_customers_repository import VacationersCustomersRepository


class VacationersCustomersService:
    def get_all(self, db: Session):
        return VacationersCustomersRepository(db).get_all()

    def get_by_id(self, db: Session, vc_id: int):
        item = VacationersCustomersRepository(db).get_by_id(vc_id)
        if not item:
            raise HTTPException(status_code=404, detail="Vacationer customer not found")
        return item

    def by_group(self, db: Session, group_id: int):
        return VacationersCustomersRepository(db).get_by_group_id(group_id)

    def by_vacation(self, db: Session, vacation_id: int):
        return VacationersCustomersRepository(db).get_by_vacation_id(vacation_id)

    def by_user(self, db: Session, user_id: int):
        return VacationersCustomersRepository(db).get_by_user_id(user_id)

    def get_unassigned(self, db: Session):
        return VacationersCustomersRepository(db).get_unassigned()

    def create(self, db: Session, payload):
        item = VacationersCustomers(
            UserID=payload.UserID,
            VacationID=payload.VacationID,
            UpdateDate=payload.UpdateDate,
            GroupMemberNumber=payload.GroupMemberNumber,
        )
        return VacationersCustomersRepository(db).create(item)

    def update(self, db: Session, vc_id: int, payload):
        repo = VacationersCustomersRepository(db)
        item = repo.get_by_id(vc_id)
        if not item:
            raise HTTPException(status_code=404, detail="Vacationer customer not found")
        if payload.GroupMemberNumber is not None:
            item.GroupMemberNumber = payload.GroupMemberNumber
        if payload.UpdateDate is not None:
            item.UpdateDate = payload.UpdateDate
        return repo.update(item)

    def delete(self, db: Session, vc_id: int):
        repo = VacationersCustomersRepository(db)
        item = repo.get_by_id(vc_id)
        if not item:
            raise HTTPException(status_code=404, detail="Vacationer customer not found")
        repo.delete(item)
        return {"deleted": True}


vc_service = VacationersCustomersService()
