import pandas as pd
from models import User, Room

def export_to_excel(assignments, db_session, filename="solution.xlsx"):
    """
    יצירת קובץ Excel של השיבוץ הסופי
    """
    data = []
    for user_id, room_id in assignments.items():
        user = db_session.get(User, user_id)
        room = db_session.get(Room, room_id)
        data.append({
            "User Name": user.Name,
            "Phone": user.Phone,
            "Room Number": room.RoomNumber,
            "Floor": room.Floor
        })
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)