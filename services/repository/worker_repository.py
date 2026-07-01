from sqlalchemy.orm import Session
from models import Worker


class WorkerRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Worker).order_by(Worker.IDCard).all()

    def get_by_id(self, worker_id: int):
        return self.db.query(Worker).filter(Worker.IDCard == worker_id).first()

    def get_by_email(self, email: str):
        return self.db.query(Worker).filter(Worker.Email.ilike(f"%{email}%")).first()

    def get_by_phone(self, phone: str):
        return self.db.query(Worker).filter(Worker.PhoneNumber.ilike(f"%{phone}%")).first()

    def get_by_authorization(self, auth_id: int):
        return self.db.query(Worker).filter(Worker.Permissions == auth_id).all()

    def create(self, worker: Worker):
        self.db.add(worker)
        self.db.commit()
        self.db.refresh(worker)
        return worker

    def update(self, worker: Worker):
        self.db.commit()
        self.db.refresh(worker)
        return worker

    def delete(self, worker: Worker):
        self.db.delete(worker)
        self.db.commit()
        return True
