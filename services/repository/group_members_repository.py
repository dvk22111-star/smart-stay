from sqlalchemy.orm import Session
from models import GroupMembers


class GroupMembersRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(GroupMembers).order_by(GroupMembers.IDOfGroupMembers).all()

    def get_by_id(self, group_member_id: int):
        return self.db.query(GroupMembers).filter(GroupMembers.IDOfGroupMembers == group_member_id).first()

    def get_by_group_id(self, group_id: int):
        return self.db.query(GroupMembers).filter(GroupMembers.GroupID == group_id).order_by(GroupMembers.IDOfGroupMembers).all()

    def get_by_telephone(self, telephone: str):
        normalized = telephone.replace(" ", "").replace("-", "")
        return self.db.query(GroupMembers).filter(GroupMembers.Telephone == normalized).all()

    def create(self, item: GroupMembers):
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def update(self, item: GroupMembers):
        self.db.commit()
        self.db.refresh(item)
        return item

    def delete(self, item: GroupMembers):
        self.db.delete(item)
        self.db.commit()
        return True
