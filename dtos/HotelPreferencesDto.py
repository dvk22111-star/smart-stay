from pydantic import BaseModel
from typing import Optional

# העדפות ברמת מלון
class HotelPreferencesDTO(BaseModel):
    HotelPreferencesID: int
    HotelID: int
    PreferenceID: int
    Price: float


class HotelPreferencesCreateDTO(BaseModel):
    HotelID: int
    PreferenceID: int
    Price: float


class HotelPreferencesUpdateDTO(BaseModel):
    Price: Optional[float] = None