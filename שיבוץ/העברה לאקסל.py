import pandas as pd

def export_assignment_to_excel(room_assignments: dict, rooms: list, customer_preferences: list, filename="room_assignment.xlsx"):
    """
    מייצא את השיבוץ לאקסל:
    - room_id
    - מספר חדר
    - רשימת משתמשים
    - ציון שביעות רצון
    """
    data = []

    # מיפוי מהיר room_id -> Room object
    room_map = {room.room_id: room for room in rooms}

    for room_id, user_ids in room_assignments.items():
        room = room_map[room_id]
        score = sum(max(0, 10 - cp.rating) for cp in customer_preferences if cp.user_id in user_ids)
        data.append({
            "Room ID": room.room_id,
            "Room Number": room.room_number,
            "Assigned Users": ", ".join(user_ids),
            "Satisfaction Score": score
        })

    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)
    print(f"Exported room assignments to {filename}")