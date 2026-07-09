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

        # If user has explicit preferences, intersect candidate rooms with those matching any preference
        prefs = user_pref_map.get(user.UserID)
        if prefs:
            matching = set()
            for p in prefs:
                matching |= pref_to_room_ids.get(p, set())
            # if matching set is non-empty, prefer that reduced set
            if matching:
                candidate_rooms = [r for r in candidate_rooms if r in matching]

        domains[user.UserID] = candidate_rooms

    return domains
