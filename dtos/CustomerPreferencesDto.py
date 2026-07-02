from pydantic import BaseModel
from typing import Optional

# העדפות של משתמש
class CustomerPreferencesDTO(BaseModel):
    CustomerPreferencesID: int
    Rating: int
    UserID: int
    PreferencesID: int
    VacationID: int


class CustomerPreferencesCreateDTO(BaseModel):
    Rating: int
    UserID: int
    PreferencesID: int
    VacationID: int


class CustomerPreferencesUpdateDTO(BaseModel):
    Rating: Optional[int] = None