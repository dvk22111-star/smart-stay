from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.dependencies import get_db
from dtos import UserDTO, UserCreateDTO, UserUpdateDTO
from services.mapper.User import user_service

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[UserDTO])
def get_all_users(db: Session = Depends(get_db)):
    return user_service.get_all(db)



@router.get("/search")
def search_users(name: str, db: Session = Depends(get_db)):
    return user_service.search_by_name(db, name)


@router.get("/credit/high")
def high_credit_users(db: Session = Depends(get_db)):
    return user_service.get_high_credit(db)


@router.get("/phone/{phone}", response_model=UserDTO)
def get_user_by_phone(phone: str, db: Session = Depends(get_db)):
    return user_service.get_by_phone(db, phone)


@router.get("/{user_id}", response_model=UserDTO)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    return user_service.get_by_id(db, user_id)


@router.post("/", response_model=UserDTO)
def create_user(payload: UserCreateDTO, db: Session = Depends(get_db)):
    return user_service.create(db, payload)


@router.put("/{user_id}", response_model=UserDTO)
def update_user(user_id: int, payload: UserUpdateDTO, db: Session = Depends(get_db)):
    return user_service.update(db, user_id, payload)

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return user_service.delete(db, user_id)
