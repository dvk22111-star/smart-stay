import enum

from sqlalchemy import Column, Integer, Enum
from sqlalchemy.orm import relationship

from database.base import Base


class PreferenceTypeEnum(enum.Enum):
    SEA_VIEW = "SEA_VIEW"
    LOW_FLOOR = "LOW_FLOOR"
    HIGH_FLOOR = "HIGH_FLOOR"
    ACCESSIBILITY = "ACCESSIBILITY"


class Preferences(Base):
    __tablename__ = "preferences"

    PreferencesID = Column(Integer, primary_key=True)

    PreferenceType = Column(Enum(PreferenceTypeEnum), nullable=False)

    customer_preferences = relationship(
        "CustomerPreferences",
        back_populates="preference"
    )

    hotel_preferences = relationship(
        "HotelPreferences",
        back_populates="preference"
    )

    room_preferences = relationship(
        "RoomPreferences",
        back_populates="preference"
    )

    