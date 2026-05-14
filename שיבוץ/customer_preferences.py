from dataclasses import dataclass

@dataclass
class CustomerPreference:
    customer_pref_id: str
    rating: int  # נמוך = הכי רצוי
    user_id: str
    preference_id: str
    vacation_id: str