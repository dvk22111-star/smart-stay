from pydantic import BaseModel
from typing import Optional

# בקשות לשותפים
class PartnerRequestsDTO(BaseModel):
    PartnerRequestID: int
    UserIDMember1: int
    UserIDMember2: int
    VacationID: int


class PartnerRequestsCreateDTO(BaseModel):
    UserIDMember1: int
    UserIDMember2: int
    VacationID: int