from sqlalchemy import (
    Column,
    Integer,
    Date,
    ForeignKey
)

from sqlalchemy.orm import relationship

from database.base import Base


class VacationersCustomers(Base):
    __tablename__ = "vacationers_customers"

    VacationIDForCustomers = Column(
        Integer,
        primary_key=True
    )

    UserID = Column(
        Integer,
        ForeignKey("users.UserID"),
        nullable=False
    )

    VacationID = Column(
        Integer,
        ForeignKey("vacations.VacationID"),
        nullable=False
    )

    UpdateDate = Column(
        Date,
        nullable=False
    )

    GroupMemberNumber = Column(
        Integer,
        nullable=True
    )

    user = relationship(
        "User",
        back_populates="vacations"
    )

    vacation = relationship(
        "Vacation",
        back_populates="customers"
    )

    placements = relationship(
        "Placement",
        back_populates="vacation_customer"
    )