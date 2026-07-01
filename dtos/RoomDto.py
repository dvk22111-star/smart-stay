from pydantic import BaseModel


class RoomBase(BaseModel):
    RoomNumber: str
    Floor: int
    HotelID: int
    NumberOfBeds: int


class RoomCreateDTO(RoomBase):
    pass


class RoomUpdateDTO(BaseModel):
    RoomNumber: str | None = None
    Floor: int | None = None
    HotelID: int | None = None
    NumberOfBeds: int | None = None


class RoomDTO(RoomBase):
    RoomID: int

    class Config:
        from_attributes = True