from sqlalchemy.orm import Session

from models import BotAnswer
from services.repository.bot_answer_repository import BotAnswerRepository


class BotAnswerService:
    def create(self, db: Session, answer: BotAnswer):
        return BotAnswerRepository(db).create(answer)

    def get_by_session(self, db: Session, session_id: int):
        return BotAnswerRepository(db).get_by_session(session_id)

    def get_latest_by_session_and_question(self, db: Session, session_id: int, question_id: str):
        return BotAnswerRepository(db).get_latest_by_session_and_question(session_id, question_id)

    def update(self, db: Session, answer: BotAnswer):
        return BotAnswerRepository(db).update(answer)


bot_answer_service = BotAnswerService()
