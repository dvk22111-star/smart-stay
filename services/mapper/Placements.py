from fastapi import HTTPException
from sqlalchemy.orm import Session

from models import Placement
from services.repository.placement_repository import PlacementRepository


class PlacementsService:
    def get_all(self, db: Session):
        return PlacementRepository(db).get_available()

    def get_by_room(self, db: Session, room_id: int):
        return PlacementRepository(db).get_by_room_id(room_id)

    def get_by_vacation(self, db: Session, vacation_id: int):
        repo = PlacementRepository(db)
        placements = repo.get_by_vacation_id(vacation_id)
        if not placements:
            return []
        return placements

    def get_available(self, db: Session):
        return PlacementRepository(db).get_available()

    def create(self, db: Session, payload):
        placement = Placement(
            RoomID=payload.RoomID,
            Price=payload.Price,
            VacationersCustomersID=payload.VacationersCustomersID,
        )
        return PlacementRepository(db).create(placement)

    def update(self, db: Session, placement_id: int, payload):
        repo = PlacementRepository(db)
        placement = repo.get_by_id(placement_id)
        if not placement:
            raise HTTPException(status_code=404, detail="Placement not found")
        if payload.RoomID is not None:
            placement.RoomID = payload.RoomID
        if payload.Price is not None:
            placement.Price = payload.Price
        if payload.VacationersCustomersID is not None:
            placement.VacationersCustomersID = payload.VacationersCustomersID
        return repo.update(placement)

    def delete(self, db: Session, placement_id: int):
        repo = PlacementRepository(db)
        placement = repo.get_by_id(placement_id)
        if not placement:
            raise HTTPException(status_code=404, detail="Placement not found")
        repo.delete(placement)
        return {"deleted": True}


placement_service = PlacementsService()
