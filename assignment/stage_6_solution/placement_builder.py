from models import Placement


def build_placements(
    assignments,
    vacation_id,
    price_lookup,
    vacation_customers
):
    """
    assignments:
        user_id -> room_id

    מחזיר רשימת Placement
    """

    placements = []

    user_to_vacationers_id = {
        vc.UserID: vc.VacationIDForCustomers
        for vc in vacation_customers
    }

    for user_id, room_id in assignments.items():

        price = price_lookup.get(
            (user_id, room_id),
            0
        )

        vacationers_customers_id = user_to_vacationers_id.get(user_id)
        if vacationers_customers_id is None:
            raise ValueError(f"No VacationersCustomers record found for user {user_id}")

        placement = Placement(
            RoomID=room_id,
            VacationersCustomersID=vacationers_customers_id,
            VacationID=vacation_id,
            Price=price
        )

        placements.append(
            placement
        )

    return placements