from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKey
)

from sqlalchemy.orm import relationship

from database.base import Base


class Worker(Base):
    __tablename__ = "workers"

    IDCard = Column(
        Integer,
        primary_key=True
    )

    Name = Column(
        String(255)
    )

    PhoneNumber = Column(
        String(20)
    )

    Email = Column(
        String(255)
    )

    Permissions = Column(
        Integer,
        ForeignKey(
            "permissions.AuthorizationID"
        )
    )

    permission = relationship(
        "Permission"
    )