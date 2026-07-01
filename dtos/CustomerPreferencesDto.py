from pydantic import BaseModel
from typing import Optional

# העדפות של משתמש
class CustomerPreferencesDTO(BaseModel):
    CustomerPreferencesID: int
    Rating: int
    UserID: int
    PreferencesID: int
    VacationID: int
    ExtraCharge: Optional[float] = None
    SurchargeAccepted: Optional[bool] = None


class CustomerPreferencesCreateDTO(BaseModel):
    Rating: int
    UserID: int
    PreferencesID: int
    VacationID: int
    ExtraCharge: Optional[float] = None
    SurchargeAccepted: Optional[bool] = None


class CustomerPreferencesUpdateDTO(BaseModel):
    Rating: Optional[int] = None