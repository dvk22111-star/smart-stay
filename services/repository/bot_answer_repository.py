from sqlalchemy.orm import Session
from models import BotAnswer


class BotAnswerRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_session(self, session_id: int):
        return self.db.query(BotAnswer).filter(BotAnswer.SessionID == session_id).order_by(BotAnswer.CreatedAt).all()

    def create(self, answer: BotAnswer):
        self.db.add(answer)
        self.db.commit()
        self.db.refresh(answer)
        return answer

    def update(self, answer: BotAnswer):
        # SQLAlchemy will persist changes on commit; assume answer is attached
        self.db.commit()
        self.db.refresh(answer)
        return answer

    def delete(self, answer: BotAnswer):
        self.db.delete(answer)
        self.db.commit()
        return True
