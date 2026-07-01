from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.dependencies import get_db
from dtos import PlacementDTO, PlacementCreateDTO, PlacementUpdateDTO
from services.mapper.Placements import placement_service

router = APIRouter(prefix="/placement", tags=["Placement"])


@router.get("/", response_model=list[PlacementDTO])
def get_all(db: Session = Depends(get_db)):
    return placement_service.get_all(db)


@router.get("/{id}", response_model=PlacementDTO)
def get_by_id(id: int, db: Session = Depends(get_db)):
    return placement_service.get_by_id(db, id)


@router.post("/", response_model=PlacementDTO)
def create(payload: PlacementCreateDTO, db: Session = Depends(get_db)):
    return placement_service.create(db, payload)


@router.put("/{id}", response_model=PlacementDTO)
def update(id: int, payload: PlacementUpdateDTO, db: Session = Depends(get_db)):
    return placement_service.update(db, id, payload)


@router.delete("/{id}")
def delete(id: int, db: Session = Depends(get_db)):
    return placement_service.delete(db, id)