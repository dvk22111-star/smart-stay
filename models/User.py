#משתמש
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database.base import Base


class User(Base):
    __tablename__ = "users"

    UserID = Column(Integer, primary_key=True, autoincrement=True)

    Name = Column(String(255), nullable=False)

    Phone = Column(String(20), unique=True, nullable=False)

    Email = Column(String(255), unique=True, nullable=False)

    Credit = Column(String(255))

    preferences = relationship(
        "CustomerPreferences",
        back_populates="user"
    )

    vacations = relationship(
        "VacationersCustomers",
        back_populates="user"
    )




