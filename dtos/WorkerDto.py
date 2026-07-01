from pydantic import BaseModel
from typing import Optional

# עובד מערכת
class WorkerDTO(BaseModel):
    IDCard: int
    Name: Optional[str]
    PhoneNumber: Optional[str]
    Email: Optional[str]
    Permissions: Optional[int]


class WorkerCreateDTO(BaseModel):
    Name: str
    PhoneNumber: str
    Email: str
    Permissions: int


class WorkerUpdateDTO(BaseModel):
    PhoneNumber: Optional[str] = None
    Email: Optional[str] = None

