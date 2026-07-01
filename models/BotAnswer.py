import json
from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship

from database.base import Base


class BotAnswer(Base):
    __tablename__ = "bot_answers"

    AnswerID = Column(Integer, primary_key=True)
    SessionID = Column(Integer, ForeignKey("bot_registration_sessions.SessionID"), nullable=False)
    QuestionID = Column(String(100), nullable=False)
    AnswerText = Column(Text, nullable=False)
    ParsedValue = Column(Text, nullable=True)
    IsFinal = Column(String(5), default="false")
    CreatedAt = Column(DateTime, default=datetime.utcnow)

    session = relationship("BotRegistrationSession", back_populates="answers")

    def set_parsed_value(self, value):
        self.ParsedValue = json.dumps(value)

    def get_parsed_value(self):
        return json.loads(self.ParsedValue) if self.ParsedValue else None
