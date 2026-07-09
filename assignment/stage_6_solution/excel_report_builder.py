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

    for user_id, room_id in assignments.items():
        user = user_map.get(user_id)
        room = room_map.get(room_id)

        if not user or not room:
            continue

        top_two_pref_ids = [
            pref.PreferencesID
            for pref in sorted(
                user_pref_map.get(user_id, []),
                key=lambda pref: pref.Rating
            )
            if pref.Rating in (1, 2)
        ]

        assigned_room_prefs = set(room_pref_map.get(room_id, []))
        matched_top_two = bool(
            set(top_two_pref_ids) & assigned_room_prefs
        )

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
                    "אין העדפה 1/2" if not top_two_pref_ids
                    else "החדר אינו תואם לעדיפות 1/2"
                ),
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
    }
