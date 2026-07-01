from pydantic import BaseModel
from typing import Optional

# חבר בקבוצה
class GroupMembersDTO(BaseModel):
    IDOfGroupMembers: int
    GroupID: int
    Telephone: str


class GroupMembersCreateDTO(BaseModel):
    GroupID: int
    Telephone: str


class GroupMembersUpdateDTO(BaseModel):
    Telephone: Optional[str] = None