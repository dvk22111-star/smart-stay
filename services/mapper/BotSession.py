from fastapi import HTTPException
from sqlalchemy.orm import Session

from models import BotRegistrationSession
from services.repository.bot_session_repository import BotSessionRepository


class BotSessionService:
    def get_by_id(self, db: Session, session_id: int):
        session = BotSessionRepository(db).get_by_id(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Bot session not found")
        return session

    def get_by_phone(self, db: Session, phone: str):
        return BotSessionRepository(db).get_by_phone(phone)

    def create(self, db: Session, payload):
        session = BotRegistrationSession(
            Phone=payload.Phone,
            VacationID=payload.VacationID,
            GroupID=payload.GroupID,
            Status="AWAITING_VERIFICATION",
        )
        return BotSessionRepository(db).create(session)

    def update_status(self, db: Session, session_id: int, status: str):
        session = self.get_by_id(db, session_id)
        session.Status = status
        return BotSessionRepository(db).update(session)

    def update_current_question(self, db: Session, session_id: int, question_id: str):
        session = self.get_by_id(db, session_id)
        session.CurrentQuestionID = question_id
        return BotSessionRepository(db).update(session)


bot_session_service = BotSessionService()
