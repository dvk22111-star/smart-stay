from dataclasses import dataclass

from ortools.sat.python import cp_model


# מחזיק את כל הנתונים של מנוע השיבוץ
# ועובר בין כל שלבי האלגוריתם
@dataclass
class AssignmentContext:

    # מודל CP-SAT
    model: cp_model.CpModel

    # משתמשים המשתתפים בנופש
    users: list

    # חדרים זמינים לשיבוץ
    rooms: list

    # משתני השיבוץ
    # (UserID, RoomID) -> BoolVar
    variables: dict

    # העדפות לקוחות
    customer_preferences: list

    # העדפות חדרים
    room_preferences: list

    # העדפות מלון
    hotel_preferences: list

    # בקשות שותפות
    partner_requests: list

    # קבוצות
    groups: list

    # חברי קבוצה
    group_members: list

    # רשומות VacationersCustomers
    vacation_customers: list

    # הנופש הנוכחי
    vacation: object
