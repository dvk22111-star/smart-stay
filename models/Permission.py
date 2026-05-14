#הרשאות
import enum

from sqlalchemy import (
    Column,
    Integer,
    Enum
)

from database.base import Base


class PermissionTypeEnum(enum.Enum):
    ADMIN = "ADMIN"
    SECRETARY = "SECRETARY"
    GROUP_MANAGER = "GROUP_MANAGER"


class Permission(Base):
    __tablename__ = "permission"

    AuthorizationID = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    AuthorizationType = Column(
        Enum(PermissionTypeEnum),
        nullable=False
    )