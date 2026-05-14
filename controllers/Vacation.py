
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from repositories.vacation_repository import VacationRepository
from services.vacation_service import VacationService
from models.vacation import Base

engine = create_engine("sqlite:///vacation.db")
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

Base.metadata.create_all(bind=engine)

vacation_repo = VacationRepository(session)
vacation_service = VacationService(vacation_repo)

def create_vacation_controller(hotel_id, start, end, program_link, basic_cost, number_of_rooms, number_of_floors):
    return vacation_service.create_vacation(hotel_id, start, end, program_link, basic_cost, number_of_rooms, number_of_floors)

def list_vacations_controller():
    return vacation_service.get_all_vacations()
