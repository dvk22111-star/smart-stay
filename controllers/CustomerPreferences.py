

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from repositories.customer_preferences_repository import CustomerPreferencesRepository
from services.customer_preferences_service import CustomerPreferencesService
from models.customer_preferences import Base

engine = create_engine("sqlite:///vacation.db")
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

Base.metadata.create_all(bind=engine)

customer_pref_repo = CustomerPreferencesRepository(session)
customer_pref_service = CustomerPreferencesService(customer_pref_repo)

def create_customer_preference_controller(rating, user_id, preferences_id, vacation_id):
    return customer_pref_service.create_customer_preference(rating, user_id, preferences_id, vacation_id)

def list_customer_preferences_controller():
    return customer_pref_service.get_all_customer_preferences()
