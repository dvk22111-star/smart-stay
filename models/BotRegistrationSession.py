import enum
from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship

from database.base import Base


class BotSessionStatusEnum(enum.Enum):
    IN_PROGRESS = "IN_PROGRESS"
    AWAITING_VERIFICATION = "AWAITING_VERIFICATION"
    COMPLETED = "COMPLETED"


class BotRegistrationSession(Base):
    __tablename__ = "bot_registration_sessions"

    SessionID = Column(Integer, primary_key=True)
    UserID = Column(Integer, ForeignKey("users.UserID"), nullable=True)
    VacationID = Column(Integer, ForeignKey("vacations.VacationID"), nullable=True)
    GroupID = Column(Integer, ForeignKey("groups.GroupID"), nullable=True)
    Phone = Column(String(20), nullable=False)
    Status = Column(Enum(BotSessionStatusEnum), nullable=False, default=BotSessionStatusEnum.IN_PROGRESS)
    CurrentQuestionID = Column(String(100), nullable=True)
    CreatedAt = Column(DateTime, default=datetime.utcnow)
    UpdatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    answers = relationship("BotAnswer", back_populates="session", cascade="all, delete-orphan")
    user = relationship("User")
    vacation = relationship("Vacation")
    group = relationship("Group")
