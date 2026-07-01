from sqlalchemy import (
    Column,
    Integer,
    Float,
    Date,
    ForeignKey,
    Text
)

from sqlalchemy.orm import relationship

from database.base import Base


class Vacation(Base):
    __tablename__ = "vacations"

    VacationID = Column(
        Integer,
        primary_key=True
    )

    HotelID = Column(
        Integer,
        ForeignKey("hotels.HotelID")
    )

    StartV = Column(
        Date,
        nullable=False
    )

    EndV = Column(
        Date,
        nullable=False
    )

    Program = Column(
        Text
    )

    BasicCost = Column(
        Float,
        nullable=False
    )

    NumberOfRooms = Column(
        Integer
    )

    NumberOfFloors = Column(
        Integer
    )

    hotel = relationship(
        "Hotel",
        back_populates="vacations"
    )

    customers = relationship(
        "VacationersCustomers",
        back_populates="vacation"
    )

    groups = relationship(
        "Group",
        back_populates="vacation"
    )