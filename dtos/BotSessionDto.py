from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime


class BotAnswerCreateDTO(BaseModel):
    QuestionID: str
    AnswerText: str
    IsFinal: Optional[bool] = False


class BotAnswerDTO(BotAnswerCreateDTO):
    AnswerID: int
    SessionID: int
    ParsedValue: Optional[Any] = None
    CreatedAt: datetime

    class Config:
        orm_mode = True


class BotSessionCreateDTO(BaseModel):
    Phone: str
    VacationID: Optional[int] = None
    GroupID: Optional[int] = None


class BotSessionDTO(BaseModel):
    SessionID: int
    UserID: Optional[int] = None
    VacationID: Optional[int] = None
    GroupID: Optional[int] = None
    Phone: str
    Status: str
    CurrentQuestionID: Optional[str] = None
    CreatedAt: datetime
    UpdatedAt: datetime
    answers: Optional[List[BotAnswerDTO]] = []

    class Config:
        orm_mode = True
