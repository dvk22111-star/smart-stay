from fastapi import HTTPException
from sqlalchemy.orm import Session

from models import Worker
from services.repository.worker_repository import WorkerRepository


class WorkerService:
    def get_all(self, db: Session):
        return WorkerRepository(db).get_all()

    def get_by_id(self, db: Session, worker_id: int):
        item = WorkerRepository(db).get_by_id(worker_id)
        if not item:
            raise HTTPException(status_code=404, detail="Worker not found")
        return item

    def get_by_email(self, db: Session, email: str):
        item = WorkerRepository(db).get_by_email(email)
        if not item:
            raise HTTPException(status_code=404, detail="Worker not found")
        return item

    def get_by_phone(self, db: Session, phone: str):
        item = WorkerRepository(db).get_by_phone(phone)
        if not item:
            raise HTTPException(status_code=404, detail="Worker not found")
        return item

    def by_authorization(self, db: Session, auth_id: int):
        return WorkerRepository(db).get_by_authorization(auth_id)

    def create(self, db: Session, payload):
        item = Worker(
            Name=payload.Name,
            PhoneNumber=payload.PhoneNumber,
            Email=payload.Email,
            Permissions=payload.Permissions,
        )
        return WorkerRepository(db).create(item)

    def update(self, db: Session, worker_id: int, payload):
        repo = WorkerRepository(db)
        item = repo.get_by_id(worker_id)
        if not item:
            raise HTTPException(status_code=404, detail="Worker not found")
        if payload.PhoneNumber is not None:
            item.PhoneNumber = payload.PhoneNumber
        if payload.Email is not None:
            item.Email = payload.Email
        if payload.Permissions is not None:
            item.Permissions = payload.Permissions
        return repo.update(item)

    def delete(self, db: Session, worker_id: int):
        repo = WorkerRepository(db)
        item = repo.get_by_id(worker_id)
        if not item:
            raise HTTPException(status_code=404, detail="Worker not found")
        repo.delete(item)
        return {"deleted": True}


worker_service = WorkerService()
