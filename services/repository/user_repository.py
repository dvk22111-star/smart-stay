from sqlalchemy.orm import Session
from models import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(User).order_by(User.UserID).all()

    def get_by_id(self, user_id: int):
        return self.db.query(User).filter(User.UserID == user_id).first()

    def get_by_phone(self, phone: str):
        return self.db.query(User).filter(User.Phone == phone).first()

    def search_by_name(self, name: str):
        return self.db.query(User).filter(User.Name.ilike(f"%{name}%")).all()

    def get_high_credit(self):
        return self.db.query(User).filter(User.Credit > 0).all()

    def create(self, user: User):
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update(self, user: User):
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user: User):
        self.db.delete(user)
        self.db.commit()
        return True
