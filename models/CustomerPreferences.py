#העדפות ללקוח
from sqlalchemy import (
    Column,
    Integer,
    ForeignKey
)
from sqlalchemy import Float, Boolean

from sqlalchemy.orm import relationship

from database.base import Base


class CustomerPreferences(Base):
    __tablename__ = "customer_preferences"

    CustomerPreferencesID = Column(
        Integer,
        primary_key=True
    )

    Rating = Column(Integer, nullable=False)

    UserID = Column(
        Integer,
        ForeignKey("users.UserID")
    )

    PreferencesID = Column(
        Integer,
        ForeignKey("preferences.PreferencesID")
    )

    VacationID = Column(
        Integer,
        ForeignKey("vacations.VacationID")
    )

    # If the preference includes a paid surcharge (e.g., sea view), record it here
    ExtraCharge = Column(
        Float,
        nullable=True
    )

    SurchargeAccepted = Column(
        Boolean,
        default=False
    )

    user = relationship(
        "User",
        back_populates="preferences"
    )

    preference = relationship(
        "Preferences",
        back_populates="customer_preferences"
    )

    vacation = relationship(
        "Vacation"
    )