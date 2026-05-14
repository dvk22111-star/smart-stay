#העדפות
import enum

from sqlalchemy import (
    Column,
    Integer,
    Enum
)

from database.base import Base


class PreferenceTypeEnum(enum.Enum):
    SEA_VIEW = "SEA_VIEW"
    QUIET = "QUIET"
    BALCONY = "BALCONY"


class Preferences(Base):
    __tablename__ = "preferences"

    PreferencesID = Column(
        Integer,
        primary_key=True
    )

    PreferenceType = Column(
        Enum(PreferenceTypeEnum),
        nullable=False
    )

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