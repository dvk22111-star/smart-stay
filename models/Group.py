#קבוצה
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean,
    ForeignKey
)

from sqlalchemy.orm import relationship

from database.base import Base


class Group(Base):
    __tablename__ = "groups"

    GroupID = Column(Integer, primary_key=True)

    UserID = Column(
        Integer,
        ForeignKey("users.UserID")
    )

    GroupName = Column(String(255))

    NumberofParticipants = Column(Integer)

    VacationID = Column(
        Integer,
        ForeignKey("vacations.VacationID")
    )

    GroupPrice = Column(Float)

    IndividualPrice = Column(Float)

    PaidAsAGroup = Column(Boolean)

    members = relationship(
        "GroupMembers",
        back_populates="group"
    )