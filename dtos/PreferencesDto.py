from pydantic import BaseModel
from enum import Enum

# סוגי העדפות
class PreferenceTypeEnum(str, Enum):
    SEA_VIEW = "SEA_VIEW"
    LOW_FLOOR = "LOW_FLOOR"
    HIGH_FLOOR = "HIGH_FLOOR"


class PreferencesDTO(BaseModel):
    PreferencesID: int
    PreferenceType: PreferenceTypeEnum


class PreferencesCreateDTO(BaseModel):
    PreferenceType: PreferenceTypeEnum