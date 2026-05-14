#חדר
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database.base import Base


class Room(Base):
    __tablename__ = "rooms"

    RoomID = Column(Integer, primary_key=True)

    RoomNumber = Column(String(50), nullable=False)

    Floor = Column(Integer, nullable=False)

    HotelID = Column(
        Integer,
        ForeignKey("hotels.HotelID")
    )

    NumberOfBeds = Column(Integer, nullable=False)

    hotel = relationship(
        "Hotel",
        back_populates="rooms"
    )

    placements = relationship(
        "Placement",
        back_populates="room"
    )

    room_preferences = relationship(
        "RoomPreferences",
        back_populates="room"
    )