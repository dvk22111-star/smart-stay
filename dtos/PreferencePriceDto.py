from pydantic import BaseModel
from typing import Optional


class PreferencePriceDTO(BaseModel):
    PreferencePriceID: int
    PreferenceID: int
    AdditionalPrice: float


class PreferencePriceCreateDTO(BaseModel):
    PreferenceID: int
    AdditionalPrice: float


class PreferencePriceUpdateDTO(BaseModel):
    AdditionalPrice: Optional[float] = None
