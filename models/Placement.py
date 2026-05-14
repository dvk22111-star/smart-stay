#מיקום
from sqlalchemy import (
    Column,
    Integer,
    Float,
    ForeignKey
)

from sqlalchemy.orm import relationship

from database.base import Base


class Placement(Base):
    __tablename__ = "placements"

    PlacementID = Column(
        Integer,
        primary_key=True
    )

    RoomID = Column(
        Integer,
        ForeignKey("rooms.RoomID")
    )

    Price = Column(Float, nullable=False)

    VacationersCustomersID = Column(
        Integer,
        ForeignKey(
            "vacationers_customers.VacationIDForCustomers"
        )
    )

    room = relationship(
        "Room",
        back_populates="placements"
    )

    vacation_customer = relationship(
        "VacationersCustomers",
        back_populates="placements"
    )

