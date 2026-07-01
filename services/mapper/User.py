from fastapi import HTTPException
from sqlalchemy.orm import Session

from models import User
from services.repository.user_repository import UserRepository


class UserService:
    def get_all(self, db: Session):
        return UserRepository(db).get_all()

    def get_by_id(self, db: Session, user_id: int):
        user = UserRepository(db).get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    def get_by_phone(self, db: Session, phone: str):
        user = UserRepository(db).get_by_phone(phone)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    def search_by_name(self, db: Session, name: str):
        return UserRepository(db).search_by_name(name)

    def get_high_credit(self, db: Session):
        return UserRepository(db).get_high_credit()

    def create(self, db: Session, payload):
        user = User(
            Name=payload.Name,
            Phone=payload.Phone,
            Email=payload.Email,
            Credit=payload.Credit or 0,
        )
        return UserRepository(db).create(user)

    def update(self, db: Session, user_id: int, payload):
        repo = UserRepository(db)
        user = repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if payload.Name is not None:
            user.Name = payload.Name
        if payload.Phone is not None:
            user.Phone = payload.Phone
        if payload.Email is not None:
            user.Email = payload.Email
        if payload.Credit is not None:
            user.Credit = payload.Credit
        return repo.update(user)

    def delete(self, db: Session, user_id: int):
        repo = UserRepository(db)
        user = repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        repo.delete(user)
        return {"deleted": True}


user_service = UserService()
