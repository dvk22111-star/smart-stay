from pydantic import BaseModel
from enum import Enum

# סוג הרשאות
class PermissionTypeEnum(str, Enum):
    ADMIN = "ADMIN"
    SECRETARY = "SECRETARY"
    GROUP_MANAGER = "GROUP_MANAGER"


class PermissionsDTO(BaseModel):
    AuthorizationID: int
    AuthorizationType: PermissionTypeEnum


class PermissionsCreateDTO(BaseModel):
    AuthorizationType: PermissionTypeEnum