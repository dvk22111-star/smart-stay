from sqlalchemy.orm import Session
from models import Permission


class PermissionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Permission).order_by(Permission.AuthorizationID).all()

    def get_by_id(self, permission_id: int):
        return self.db.query(Permission).filter(Permission.AuthorizationID == permission_id).first()

    def get_by_type(self, auth_type: str):
        return self.db.query(Permission).filter(Permission.AuthorizationType.ilike(f"%{auth_type}%")).all()

    def create(self, permission: Permission):
        self.db.add(permission)
        self.db.commit()
        self.db.refresh(permission)
        return permission

    def update(self, permission: Permission):
        self.db.commit()
        self.db.refresh(permission)
        return permission

    def delete(self, permission: Permission):
        self.db.delete(permission)
        self.db.commit()
        return True
