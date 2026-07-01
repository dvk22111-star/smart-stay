from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    Name: str
    Phone: str
    Email: str
    Credit: Optional[float] = 0


class UserCreateDTO(UserBase):
    """יצירת משתמש חדש"""
    pass


class UserUpdateDTO(BaseModel):
    """עדכון משתמש"""
    Name: Optional[str] = None
    Phone: Optional[str] = None
    Email: Optional[str] = None
    Credit: Optional[float] = None


class UserDTO(UserBase):
    """החזרת משתמש"""
    UserID: int

    class Config:
        from_attributes = True