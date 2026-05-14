from dataclasses import dataclass

@dataclass
class Group:
    group_id: str
    admin_user_id: str
    group_name: str
    number_of_participants: int
    vacation_id: str
    group_price: float
    individual_price: float
    paid_as_group: bool