
from services.user_service import UserService
from repositories.user_repository import UserRepository
from models.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///vacation.db")
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

user_repo = UserRepository(session)
user_service = UserService(user_repo)

def create_user_controller(name, phone, email, credit):
    return user_service.create_user(name, phone, email, credit)

def list_users_controller():
    return user_service.get_all_users()

