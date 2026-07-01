from pydantic import BaseModel
from datetime import date
from typing import Optional


class VacationBase(BaseModel):
    HotelID: int
    StartV: date
    EndV: date
    Program: Optional[str]
    BasicCost: float
    NumberOfRooms: int
    NumberOfFloors: int


class VacationCreateDTO(VacationBase):
    pass


class VacationUpdateDTO(BaseModel):
    HotelID: int | None = None
    StartV: date | None = None
    EndV: date | None = None
    Program: str | None = None
    BasicCost: float | None = None
    NumberOfRooms: int | None = None
    NumberOfFloors: int | None = None


class VacationDTO(VacationBase):
    VacationID: int

    class Config:
        from_attributes = True