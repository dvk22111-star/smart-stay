import os
from collections import defaultdict

from models import Room, User


def build_report_tables(
    assignments,
    users,
    rooms,
    group_members,
    customer_preferences,
    room_preferences,
    partner_requests,
):
    """בונה את טבלאות הדוח לייצוא ולאנשי הקשר הפנימיים."""

    user_map = {user.UserID: user for user in users}
    room_map = {room.RoomID: room for room in rooms}

    room_pref_map = defaultdict(list)
    for rp in room_preferences:
        room_pref_map[rp.RoomID].append(rp.IDPreferences)

    user_pref_map = defaultdict(list)
    for pref in customer_preferences:
        user_pref_map[pref.UserID].append(pref)

    assigned_by_room = defaultdict(list)
    for user_id, room_id in assignments.items():
        assigned_by_room[room_id].append(user_id)

    assignment_rows = []
    low_score_rows = []
    unmet_partner_rows = []

    for user_id, room_id in assignments.items():
        user = user_map.get(user_id)
        room = room_map.get(room_id)

        if not user or not room:
            continue

        # בוחרים את שתי ההעדפות החזקות ביותר (לפי Rating, יורד)
        user_prefs = list(user_pref_map.get(user_id, []))
        user_prefs_sorted = sorted(user_prefs, key=lambda p: getattr(p, 'Rating', 0), reverse=True)
        top_two = user_prefs_sorted[:2]

        # אחיד את השם של השדה שמייצג את מזהה ההעדפה (יכול להיות PreferencesID או IDPreferences)
        def pref_id_of(p):
            return getattr(p, 'PreferencesID', None) or getattr(p, 'IDPreferences', None)

        top_two_pref_ids = [pref_id_of(p) for p in top_two if pref_id_of(p) is not None]

        assigned_room_prefs = set(room_pref_map.get(room_id, []))
        matched_top_two = False
        if top_two_pref_ids:
            matched_top_two = bool(set(top_two_pref_ids) & assigned_room_prefs)

        assignment_rows.append({
            "User Name": user.Name,
            "Phone": user.Phone,
            "Room Number": room.RoomNumber,
            "Floor": room.Floor,
            "Assigned Room Capacity": room.NumberOfBeds,
            "Matched Top-2 Preference": "Yes" if matched_top_two else "No",
            "Top-2 Preferences Count": len(top_two_pref_ids),
        })

        if not matched_top_two:
            low_score_rows.append({
                "User Name": user.Name,
                "Phone": user.Phone,
                "Room Number": room.RoomNumber,
                "Floor": room.Floor,
                "Notes": (
                    "אין העדפה ב-Top2" if not top_two_pref_ids
                    else "החדר אינו תואם לעדיפות Top2"
                ),
            })

    # בדיקת בקשות שותפים שלא מומשו: עבור כל בקשה בו שני המשתתפים לא שותפו באותו חדר
    for req in partner_requests:
        u1 = getattr(req, 'UserIDMember1', None)
        u2 = getattr(req, 'UserIDMember2', None)
        if u1 is None or u2 is None:
            continue

        r1 = assignments.get(u1)
        r2 = assignments.get(u2)

        # אם אחד מהם לא שובץ או ה-room_id שונה — הבקשה לא מומשה
        if r1 is None or r2 is None or r1 != r2:
            user1 = user_map.get(u1)
            user2 = user_map.get(u2)
            unmet_partner_rows.append({
                "User1": user1.Name if user1 else str(u1),
                "User2": user2.Name if user2 else str(u2),
                "User1 Room": room_map.get(r1).RoomNumber if (r1 and room_map.get(r1)) else None,
                "User2 Room": room_map.get(r2).RoomNumber if (r2 and room_map.get(r2)) else None,
                "Notes": "Partner request not satisfied",
            })

            # הוסף גם לשורות low_score לכל משתמש בבקשה לא מומשה (לדיווח JSON)
            if user1:
                low_score_rows.append({
                    "User Name": user1.Name,
                    "Phone": user1.Phone,
                    "Room Number": room_map.get(r1).RoomNumber if (r1 and room_map.get(r1)) else None,
                    "Floor": room_map.get(r1).Floor if (r1 and room_map.get(r1)) else None,
                    "Notes": "Partner request not satisfied",
                })
            if user2:
                low_score_rows.append({
                    "User Name": user2.Name,
                    "Phone": user2.Phone,
                    "Room Number": room_map.get(r2).RoomNumber if (r2 and room_map.get(r2)) else None,
                    "Floor": room_map.get(r2).Floor if (r2 and room_map.get(r2)) else None,
                    "Notes": "Partner request not satisfied",
                })

    empty_rooms_rows = []
    free_beds_rows = []
    for room in rooms:
        assigned_count = len(assigned_by_room.get(room.RoomID, []))
        free_beds = room.NumberOfBeds - assigned_count

        if free_beds == room.NumberOfBeds:
            empty_rooms_rows.append({
                "Room Number": room.RoomNumber,
                "Floor": room.Floor,
                "Beds": room.NumberOfBeds,
            })

        if free_beds > 0:
            free_beds_rows.append({
                "Room Number": room.RoomNumber,
                "Floor": room.Floor,
                "Free Beds": free_beds,
                "Total Beds": room.NumberOfBeds,
            })

    registered_phones = {
        user.Phone
        for user in users
        if user.Phone
    }

    missing_women_rows = []
    for member in group_members:
        if member.Telephone not in registered_phones:
            missing_women_rows.append({
                "Group ID": member.GroupID,
                "Telephone": member.Telephone,
            })

    return {
        "assignments": assignment_rows,
        "empty_rooms": empty_rooms_rows,
        "free_beds": free_beds_rows,
        "missing_women": missing_women_rows,
        "low_score_women": low_score_rows,
        "unmet_partner_requests": unmet_partner_rows,
    }
