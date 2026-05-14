#בקשות לשותף
from sqlalchemy import (
    Column,
    Integer,
    ForeignKey
)

from database.base import Base


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