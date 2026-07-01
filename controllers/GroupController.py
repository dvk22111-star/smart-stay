from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from database.dependencies import get_db
from dtos import GroupDTO
from services.mapper.Group import group_service

router = APIRouter(prefix="/groups", tags=["Groups"])

@router.get("/", response_model=List[GroupDTO])
def get_all(db: Session = Depends(get_db)):
    return group_service.get_all(db)

@router.get("/vacation/{vacation_id}")
def by_vacation(vacation_id: int, db: Session = Depends(get_db)):
    return group_service.by_vacation(db, vacation_id)

@router.get("/size/{min_size}")
def large_groups(min_size: int, db: Session = Depends(get_db)):
    return group_service.get_by_min_size(db, min_size)
