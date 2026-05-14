

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from repositories.preferences_repository import PreferencesRepository
from services.preferences_service import PreferencesService
from models.preferences import Base, PreferenceTypeEnum

engine = create_engine("sqlite:///vacation.db")
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

Base.metadata.create_all(bind=engine)

preferences_repo = PreferencesRepository(session)
preferences_service = PreferencesService(preferences_repo)

def create_preference_controller(preference_type: PreferenceTypeEnum):
    return preferences_service.create_preference(preference_type)

def list_preferences_controller():
    return preferences_service.get_all_preferences()
