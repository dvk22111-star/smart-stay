from pydantic import BaseModel
from typing import Optional

# DTO שמייצג קבוצה
class GroupDTO(BaseModel):
    GroupID: int
    UserID: int
    GroupName: Optional[str]
    NumberofParticipants: Optional[int]
    VacationID: int
    GroupPrice: Optional[float]
    IndividualPrice: Optional[float]
    PaidAsAGroup: Optional[bool]


class GroupCreateDTO(BaseModel):
    GroupName: str
    UserID: int
    VacationID: int


class GroupUpdateDTO(BaseModel):
    GroupName: Optional[str] = None
    NumberofParticipants: Optional[int] = None
    GroupPrice: Optional[float] = None
    IndividualPrice: Optional[float] = None
    PaidAsAGroup: Optional[bool] = None