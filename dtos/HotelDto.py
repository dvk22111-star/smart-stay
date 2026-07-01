from pydantic import BaseModel


class HotelBase(BaseModel):
    Name: str
    Address: str
    Kosher: bool
    ContactPerson: str


class HotelCreateDTO(HotelBase):
    pass


class HotelUpdateDTO(BaseModel):
    Name: str | None = None
    Address: str | None = None
    Kosher: bool | None = None
    ContactPerson: str | None = None


class HotelDTO(HotelBase):
    HotelID: int

    class Config:
        from_attributes = True