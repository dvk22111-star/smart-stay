from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from database.dependencies import get_db
from dtos import WorkerDTO, WorkerCreateDTO, WorkerUpdateDTO
from services.mapper.Worker import worker_service

router = APIRouter(prefix="/workers", tags=["Workers"])

@router.get("/", response_model=List[WorkerDTO])
def get_all_workers(db: Session = Depends(get_db)):
    return worker_service.get_all(db)

@router.get("/{worker_id}", response_model=WorkerDTO)
def get_worker_by_id(worker_id: int, db: Session = Depends(get_db)):
    return worker_service.get_by_id(db, worker_id)

@router.get("/by_role/{role}", response_model=List[WorkerDTO])
def get_workers_by_role(role: str, db: Session = Depends(get_db)):
    return worker_service.by_role(db, role)

@router.post("/", response_model=WorkerDTO)
def create_worker(worker_create: WorkerCreateDTO, db: Session = Depends(get_db)):
    return worker_service.create(db, worker_create)

@router.put("/{worker_id}", response_model=WorkerDTO)
def update_worker(worker_id: int, worker_update: WorkerUpdateDTO, db: Session = Depends(get_db)):
    return worker_service.update(db, worker_id, worker_update)

@router.delete("/{worker_id}")
def delete_worker(worker_id: int, db: Session = Depends(get_db)):
    return worker_service.delete(db, worker_id)

@router.get("/by_email/{email}", response_model=WorkerDTO)
def get_worker_by_email(email: str, db: Session = Depends(get_db)):
    return worker_service.get_by_email(db, email)

@router.get("/by_phone/{phone}", response_model=WorkerDTO)
def get_worker_by_phone(phone: str, db: Session = Depends(get_db)):
    return worker_service.get_by_phone(db, phone)
