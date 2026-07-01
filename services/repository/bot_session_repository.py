from sqlalchemy.orm import Session
from models import BotRegistrationSession


class BotSessionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, session_id: int):
        return self.db.query(BotRegistrationSession).filter(BotRegistrationSession.SessionID == session_id).first()

    def get_by_phone(self, phone: str):
        return self.db.query(BotRegistrationSession).filter(BotRegistrationSession.Phone == phone).order_by(BotRegistrationSession.CreatedAt.desc()).first()

    def create(self, session: BotRegistrationSession):
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session

    def update(self, session: BotRegistrationSession):
        self.db.commit()
        self.db.refresh(session)
        return session

    def delete(self, session: BotRegistrationSession):
        self.db.delete(session)
        self.db.commit()
        return True
