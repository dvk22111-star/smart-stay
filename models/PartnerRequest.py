#בקשות לשותף
from sqlalchemy import (
    Column,
    Integer,
    ForeignKey
)

from database.base import Base
from sqlalchemy.orm import relationship


class PartnerRequest(Base):
    __tablename__ = "partner_requests"

    PartnerRequestID = Column(
        Integer,
        primary_key=True
    )

    UserIDMember1 = Column(
        Integer,
        ForeignKey("users.UserID")
    )

    UserIDMember2 = Column(
        Integer,
        ForeignKey("users.UserID")
    )

    VacationID = Column(
        Integer,
        ForeignKey("vacations.VacationID")
    )

    member1 = relationship(
        "User",
        foreign_keys=[UserIDMember1]
    )

    member2 = relationship(
        "User",
        foreign_keys=[UserIDMember2]
    )

    vacation = relationship(
        "Vacation"
    )