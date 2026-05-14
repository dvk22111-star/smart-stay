#חבר בקבוצה
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey
)

from sqlalchemy.orm import relationship

from database.base import Base


class GroupMembers(Base):
    __tablename__ = "group_members"

    IDOfGroupMembers = Column(
        Integer,
        primary_key=True
    )

    GroupID = Column(
        Integer,
        ForeignKey("groups.GroupID")
    )

    Telephone = Column(
        String(20),
        nullable=False
    )

    group = relationship(
        "Group",
        back_populates="members"
    )