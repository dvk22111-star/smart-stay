from sqlalchemy.orm import Session
from models import Group


class GroupRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Group).order_by(Group.GroupID).all()

    def get_by_id(self, group_id: int):
        return self.db.query(Group).filter(Group.GroupID == group_id).first()

    def get_by_vacation_id(self, vacation_id: int):
        return self.db.query(Group).filter(Group.VacationID == vacation_id).order_by(Group.GroupID).all()

    def get_by_user_id(self, user_id: int):
        return self.db.query(Group).filter(Group.UserID == user_id).order_by(Group.GroupID).all()

    def get_by_min_size(self, min_size: int):
        return self.db.query(Group).filter(Group.NumberofParticipants >= min_size).all()

    def create(self, group: Group):
        self.db.add(group)
        self.db.commit()
        self.db.refresh(group)
        return group

    def update(self, group: Group):
        self.db.commit()
        self.db.refresh(group)
        return group

    def delete(self, group: Group):
        self.db.delete(group)
        self.db.commit()
        return True
