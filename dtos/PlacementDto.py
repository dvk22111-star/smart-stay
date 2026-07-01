from pydantic import BaseModel
from typing import Optional

# שיוך משתמש לחדר
class PlacementDTO(BaseModel):
    PlacementID: int
    RoomID: int
    Price: float
    VacationersCustomersID: int


class PlacementCreateDTO(BaseModel):
    RoomID: int
    VacationersCustomersID: int
    Price: float


class PlacementUpdateDTO(BaseModel):
    RoomID: Optional[int] = None
    Price: Optional[float] = None