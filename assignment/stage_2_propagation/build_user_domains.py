def build_user_domains(users, rooms, customer_prefs, room_prefs):
    """
    מחזיר dict:
        user_id -> רשימת חדרים אפשריים

    השיטה מאפשרת שיבוץ חלקי וללא סינון קשיח לפי כל ההעדפות.
    כל חדר עם קיבולת בסיסית נחשב אפשרי, והעדפות יושתו בפונקציית המטרה.
    """
    domains = {}

    for user in users:

        possible_rooms = [
            room.RoomID
            for room in rooms
            if room.NumberOfBeds >= 1
        ]

        domains[user.UserID] = possible_rooms

    return domains
