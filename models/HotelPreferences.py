#העדפות במלון
from sqlalchemy import (
    Column,
    Integer,
    Float,
    ForeignKey
)

from sqlalchemy.orm import relationship

from database.base import Base
class HotelPreferences(Base):
    __tablename__ = "hotel_preferences"

    HotelPreferencesID = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    HotelID = Column(
        Integer,
        ForeignKey("hotels.HotelID"),
        nullable=False
    )

    PreferenceID = Column(
        Integer,
        ForeignKey("preferences.PreferencesID"),
        nullable=False
    )

    Price = Column(
        Float,
        nullable=False
    )

    hotel = relationship(
        "Hotel",
        back_populates="preferences"
    )

    preference = relationship(
        "Preferences",
        back_populates="hotel_preferences"
    )
