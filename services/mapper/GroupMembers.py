from fastapi import HTTPException
from sqlalchemy.orm import Session

from models import GroupMembers
from services.repository.group_members_repository import GroupMembersRepository


class GroupMembersService:
    def get_all(self, db: Session):
        return GroupMembersRepository(db).get_all()

    def get_by_id(self, db: Session, group_member_id: int):
        item = GroupMembersRepository(db).get_by_id(group_member_id)
        if not item:
            raise HTTPException(status_code=404, detail="Group member not found")
        return item

    def by_group(self, db: Session, group_id: int):
        return GroupMembersRepository(db).get_by_group_id(group_id)

    def create(self, db: Session, payload):
        item = GroupMembers(
            GroupID=payload.GroupID,
            Telephone=payload.Telephone,
        )
        return GroupMembersRepository(db).create(item)

    def update(self, db: Session, group_member_id: int, payload):
        repo = GroupMembersRepository(db)
        item = repo.get_by_id(group_member_id)
        if not item:
            raise HTTPException(status_code=404, detail="Group member not found")
        if payload.Telephone is not None:
            item.Telephone = payload.Telephone
        return repo.update(item)

    def delete(self, db: Session, group_member_id: int):
        repo = GroupMembersRepository(db)
        item = repo.get_by_id(group_member_id)
        if not item:
            raise HTTPException(status_code=404, detail="Group member not found")
        repo.delete(item)
        return {"deleted": True}


group_members_service = GroupMembersService()
