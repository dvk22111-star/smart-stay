from pydantic import BaseModel
from typing import Optional

# העדפות חדר
class RoomPreferencesDTO(BaseModel):
    RoomPreferencesID: int
    RoomID: int
    IDPreferences: int


class RoomPreferencesCreateDTO(BaseModel):
    RoomID: int
    IDPreferences: int


class RoomPreferencesUpdateDTO(BaseModel):
    RoomID: Optional[int] = None
    IDPreferences: Optional[int] = None