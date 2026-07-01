from fastapi import HTTPException
from sqlalchemy.orm import Session

from models import Group
from services.repository.group_repository import GroupRepository


class GroupService:
    def get_all(self, db: Session):
        return GroupRepository(db).get_all()

    def get_by_id(self, db: Session, group_id: int):
        item = GroupRepository(db).get_by_id(group_id)
        if not item:
            raise HTTPException(status_code=404, detail="Group not found")
        return item

    def by_vacation(self, db: Session, vacation_id: int):
        return GroupRepository(db).get_by_vacation_id(vacation_id)

    def by_user(self, db: Session, user_id: int):
        return GroupRepository(db).get_by_user_id(user_id)

    def get_by_min_size(self, db: Session, min_size: int):
        return GroupRepository(db).get_by_min_size(min_size)

    def create(self, db: Session, payload):
        item = Group(
            UserID=payload.UserID,
            GroupName=payload.GroupName,
            NumberofParticipants=payload.NumberofParticipants,
            VacationID=payload.VacationID,
            GroupPrice=payload.GroupPrice,
            IndividualPrice=payload.IndividualPrice,
            PaidAsAGroup=payload.PaidAsAGroup,
        )
        return GroupRepository(db).create(item)

    def update(self, db: Session, group_id: int, payload):
        repo = GroupRepository(db)
        item = repo.get_by_id(group_id)
        if not item:
            raise HTTPException(status_code=404, detail="Group not found")
        if payload.GroupName is not None:
            item.GroupName = payload.GroupName
        if payload.NumberofParticipants is not None:
            item.NumberofParticipants = payload.NumberofParticipants
        if payload.VacationID is not None:
            item.VacationID = payload.VacationID
        if payload.GroupPrice is not None:
            item.GroupPrice = payload.GroupPrice
        if payload.IndividualPrice is not None:
            item.IndividualPrice = payload.IndividualPrice
        if payload.PaidAsAGroup is not None:
            item.PaidAsAGroup = payload.PaidAsAGroup
        return repo.update(item)

    def delete(self, db: Session, group_id: int):
        repo = GroupRepository(db)
        item = repo.get_by_id(group_id)
        if not item:
            raise HTTPException(status_code=404, detail="Group not found")
        repo.delete(item)
        return {"deleted": True}


group_service = GroupService()
