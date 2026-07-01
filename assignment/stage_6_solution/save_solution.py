from models import Placement
from sqlalchemy.orm import Session


def save_solution(
    session: Session,
    assignments: dict,
    vacation_id: int,
    price_lookup: dict
):

    for user_id, room_id in assignments.items():

        placement = Placement(
            RoomID=room_id,
            VacationersCustomersID=user_id,
            VacationID=vacation_id,
            Price=price_lookup.get(
                (user_id, room_id),
                0
            )
        )

        session.add(
            placement
        )

    session.commit()