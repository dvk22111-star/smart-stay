from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from database.dependencies import get_db
from dtos import GroupMembersDTO
from services.mapper.GroupMembers import group_members_service

router = APIRouter(prefix="/group-members", tags=["Group Members"])

@router.get("/", response_model=List[GroupMembersDTO])
def get_all(db: Session = Depends(get_db)):
    return group_members_service.get_all(db)

@router.get("/group/{group_id}")
def by_group(group_id: int, db: Session = Depends(get_db)):
    return group_members_service.by_group(db, group_id)
