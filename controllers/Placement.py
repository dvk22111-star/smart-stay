
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from repositories.placement_repository import PlacementRepository
from services.placement_service import PlacementService
from models.placement import Base

engine = create_engine("sqlite:///vacation.db")
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

Base.metadata.create_all(bind=engine)

placement_repo = PlacementRepository(session)
placement_service = PlacementService(placement_repo)

def create_placement_controller(room_id, price, vacationers_customers_id):
    return placement_service.create_placement(room_id, price, vacationers_customers_id)

def list_placements_controller():
    return placement_service.get_all_placements()
