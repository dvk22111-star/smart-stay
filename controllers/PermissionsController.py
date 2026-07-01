from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.dependencies import get_db
from dtos import PermissionsDTO, PermissionsCreateDTO#, PermissionsUpdateDTO
from services.mapper.Permission import permission_service

router = APIRouter(prefix="/permissions", tags=["Permissions"])


@router.get("/", response_model=list[PermissionsDTO])
def get_all(db: Session = Depends(get_db)):
    return permission_service.get_all(db)


@router.get("/{id}", response_model=PermissionsDTO)
def get_by_id(id: int, db: Session = Depends(get_db)):
    return permission_service.get_by_id(db, id)


@router.post("/", response_model=PermissionsDTO)
def create(payload: PermissionsCreateDTO, db: Session = Depends(get_db)):
    return permission_service.create(db, payload)


#@router.put("/{id}", response_model=PermissionsDTO)
#def update(id: int, payload: PermissionsUpdateDTO, db: Session = Depends(get_db)):
#    return permissions_service.update(db, id, payload)


@router.delete("/{id}")
def delete(id: int, db: Session = Depends(get_db)):
    return permission_service.delete(db, id)