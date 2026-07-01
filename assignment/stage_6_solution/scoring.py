def calculate_assignment_score(user, room, customer_prefs, room_prefs):
    """
    מחשב ציון עבור התאמת משתמש לחדר
    """
    score = 0

    # בדיקה מול העדפות הלקוח
    user_pref = [p for p in customer_prefs if p.UserID == user.UserID]
    room_pref = [p for p in room_prefs if p.RoomID == room.RoomID]

    for up in user_pref:
        for rp in room_pref:
            if rp.IDPreferences == up.PreferencesID:
                # דירוג נמוך = יותר רצוי
                score += 100 - up.Rating

    return score