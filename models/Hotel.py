#מלון
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from database.base import Base


class Hotel(Base):
    __tablename__ = "hotels"

    HotelID = Column(Integer, primary_key=True)

    Name = Column(String(255), nullable=False)

    Address = Column(String(500), nullable=False)

    Kosher = Column(Boolean, default=False)

    ContactPerson = Column(String(255))

    rooms = relationship(
        "Room",
        back_populates="hotel"
    )

    vacations = relationship(
        "Vacation",
        back_populates="hotel"
    )

    preferences = relationship(
        "HotelPreferences",
        back_populates="hotel"
    )