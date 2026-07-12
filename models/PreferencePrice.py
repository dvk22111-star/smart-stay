from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

from database.base import Base


class PreferencePrice(Base):
    __tablename__ = "preference_prices"

    PreferencePriceID = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    PreferenceID = Column(
        Integer,
        ForeignKey("preferences.PreferencesID"),
        nullable=False
    )

    AdditionalPrice = Column(
        Float,
        nullable=False
    )

    preference = relationship(
        "Preferences",
        back_populates="preference_prices"
    )
