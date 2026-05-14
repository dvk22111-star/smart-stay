#עובד
from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKey
)

from database.base import Base


class Worker(Base):
    __tablename__ = "workers"

    IDCard = Column(
        String(20),
        primary_key=True
    )

    Name = Column(String(255))

    PhoneNumber = Column(String(20))

    Email = Column(String(255))

    Authorization = Column(
        Integer,
        ForeignKey("authorization.AuthorizationID")
    )