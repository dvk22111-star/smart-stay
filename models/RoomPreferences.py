#העדפות לחדר
from sqlalchemy import (
    Column,
    Integer,
    ForeignKey
)

from sqlalchemy.orm import relationship

from database.base import Base


class RoomPreferences(Base):
    __tablename__ = "room_preferences"

    RoomPreferencesID = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    RoomID = Column(
        Integer,
        ForeignKey("rooms.RoomID"),
        nullable=False
    )

    IDPreferences = Column(
        Integer,
        ForeignKey("preferences.PreferencesID"),
        nullable=False
    )

    room = relationship(
        "Room",
        back_populates="room_preferences"
    )

    preference = relationship(
        "Preferences",
        back_populates="room_preferences"
    )