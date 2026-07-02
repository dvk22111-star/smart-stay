def build_user_domains(users, rooms, customer_prefs, room_prefs):
    """
    מחזיר dict:
        user_id -> רשימת חדרים אפשריים
    """
    domains = {}

    for user in users:

        possible_rooms = []

        for room in rooms:

            if room.NumberOfBeds < 1:
                continue

            user_pref = [
                p for p in customer_prefs
                if p.UserID == user.UserID
            ]

            room_pref = [
                p for p in room_prefs
                if p.RoomID == room.RoomID
            ]

            allowed = True

            for up in user_pref:

                if not any(
                    rp.IDPreferences == up.PreferencesID
                    for rp in room_pref
                ):
                    allowed = False
                    break

            if allowed:
                possible_rooms.append(
                    room.RoomID
                )

        domains[user.UserID] = possible_rooms

    return domains
