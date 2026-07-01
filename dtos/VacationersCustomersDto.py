from pydantic import BaseModel
from typing import Optional
from datetime import date

# שיוך משתמש לנופש
class VacationersCustomersDTO(BaseModel):
    VacationIDForCustomers: int
    UserID: int
    VacationID: int
    UpdateDate: date
    GroupMemberNumber: Optional[int]


class VacationersCustomersCreateDTO(BaseModel):
    UserID: int
    VacationID: int
    UpdateDate: date
    GroupMemberNumber: Optional[int] = None


class VacationersCustomersUpdateDTO(BaseModel):
    GroupMemberNumber: Optional[int] = None
    UpdateDate: Optional[date] = None