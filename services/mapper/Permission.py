from fastapi import HTTPException
from sqlalchemy.orm import Session

from models import Permission
from services.repository.permission_repository import PermissionRepository


class PermissionService:
    def get_all(self, db: Session):
        return PermissionRepository(db).get_all()

    def get_by_id(self, db: Session, permission_id: int):
        item = PermissionRepository(db).get_by_id(permission_id)
        if not item:
            raise HTTPException(status_code=404, detail="Permission not found")
        return item

    def by_type(self, db: Session, type_name: str):
        return PermissionRepository(db).get_by_type(type_name)

    def create(self, db: Session, payload):
        item = Permission(
            AuthorizationType=payload.AuthorizationType,
        )
        return PermissionRepository(db).create(item)

    def update(self, db: Session, permission_id: int, payload):
        repo = PermissionRepository(db)
        item = repo.get_by_id(permission_id)
        if not item:
            raise HTTPException(status_code=404, detail="Permission not found")
        if payload.AuthorizationType is not None:
            item.AuthorizationType = payload.AuthorizationType
        return repo.update(item)

    def delete(self, db: Session, permission_id: int):
        repo = PermissionRepository(db)
        item = repo.get_by_id(permission_id)
        if not item:
            raise HTTPException(status_code=404, detail="Permission not found")
        repo.delete(item)
        return {"deleted": True}


permission_service = PermissionService()
