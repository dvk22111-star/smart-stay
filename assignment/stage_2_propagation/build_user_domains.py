def build_user_domains(users, rooms, customer_prefs, room_prefs):
    """
    מחזיר dict:
        user_id -> רשימת חדרים אפשריים

    השיטה מאפשרת שיבוץ חלקי וללא סינון קשיח לפי כל ההעדפות.
    כל חדר עם קיבולת בסיסית נחשב אפשרי, והעדפות יושתו בפונקציית המטרה.
    """
    domains = {}

    # Build quick lookup maps for preferences to rooms
    pref_to_room_ids = {}
    for rp in room_prefs:
        pref_to_room_ids.setdefault(rp.IDPreferences, set()).add(rp.RoomID)

    user_pref_map = {}
    for cp in customer_prefs:
        user_pref_map.setdefault(cp.UserID, []).append(cp.PreferencesID)

    for user in users:
        # Start with rooms that have at least one bed
        candidate_rooms = [room.RoomID for room in rooms if getattr(room, 'NumberOfBeds', 1) >= 1]

        # Do NOT reduce domains based on preferences.
        # Preferences are soft and accounted for in Stage 5 optimization.
        # Keep the full set of candidate rooms (rooms with at least one bed)
        # so the solver can use multiple adjacent rooms to satisfy groups.

        domains[user.UserID] = candidate_rooms

    return domains
