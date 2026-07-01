from sqlalchemy import (
    Column,
    Integer,
    String,
    Numeric
)

from sqlalchemy.orm import relationship

from database.base import Base


class User(Base):
    __tablename__ = "users"

    UserID = Column(
        Integer,
        primary_key=True
    )

    Name = Column(
        String(255),
        nullable=False
    )

    Phone = Column(
        String(20),
        unique=True,
        nullable=False
    )

    Email = Column(
        String(255),
        unique=True,
        nullable=False
    )

    Credit = Column(
        Numeric(10, 2),
        default=0
    )

    preferences = relationship(
        "CustomerPreferences",
        back_populates="user"
    )

    vacations = relationship(
        "VacationersCustomers",
        back_populates="user"
    )

    group_admin = relationship(
        "Group",
        backref="admin"
    )



