
#הצעה בסיסית של התכתבות עם בוט





# chat_bot.py
import datetime

# נתונים לדוגמה655555555
HOTELS = {
    "גלי צאנז": {"rooms": 10, "accessible": True},
    "גלי התמר": {"rooms": 5, "accessible": False}
}

COUPONS = {
    "WELCOME10": 10,  # אחוז הנחה
    "VIP50": 50
}

# דוגמה לסטטוס הזמנות
BOOKINGS = []

def get_available_dates():
    return ["11/07", "21/08"]

def respond_to_user(user_input, user_data):
    response = ""

    # זיהוי סוג בקשה
    if "תאריך" in user_input or "נופש" in user_input:
        dates = get_available_dates()
        response += f"יש לי נופשים בתאריכים הבאים: {', '.join(dates)}. לאיזה מהם את מעוניינת?\n"
        response += "אפשר לבחור בין מסלול פרימיום ליום אחד או מסלול בוטיק עם לינה.\n"
        response += "מה שמך המלא, כתובת דוא\"ל ומספר טלפון?\n"

    elif "מלון" in user_input:
        hotel_name = [name for name in HOTELS.keys() if name in user_input]
        if hotel_name:
            hotel = hotel_name[0]
            if HOTELS[hotel]["rooms"] > 0:
                response += f"יש לנו חדרים פנויים ב-{hotel}. האם את מעוניינת להזמין?\n"
            else:
                response += f"אין חדרים פנויים ב-{hotel} בתאריך זה, אבל יש לנו חלופות במלון אחר.\n"
        else:
            response += "אני לא מזהה את שם המלון שהזנת, אנא הזיני שוב.\n"

    elif "החזרי לידה" in user_input:
        response += "יש לנו החזרי לידה, הפרטים מול המלון יש לבדוק ישירות.\n"

    elif "הסדר" in user_input:
        response += "כרגע אין הסדר עם השם שביקשת, אנו מקווים להוסיף בעתיד.\n"

    elif "מחיר" in user_input or "הצעת מחיר" in user_input:
        # חישוב מחיר בסיסי עם קופון
        base_price = 500  # דוגמה
        if "קופון" in user_input:
            coupon_code = user_input.split()[-1]
            discount = COUPONS.get(coupon_code.upper(), 0)
            base_price = base_price * (1 - discount / 100)
            response += f"המחיר לאחר הנחת הקופון {coupon_code}: {base_price} ש\"ח.\n"
        else:
            response += f"המחיר הכולל: {base_price} ש\"ח.\n"

    elif "נכה" in user_input or "מונגש" in user_input:
        response += "יש לנו חדרים מונגשים בהתאם לדרישות.\n"

    else:
        response += "אני לא מבין את הבקשה, אנא נסי לשאול בצורה אחרת.\n"

    return response

# דוגמת שימוש
if __name__ == "__main__":
    user_data = {}
    while True:
        user_input = input("משתמש: ")
        if user_input.lower() in ["יציאה", "סיים"]:
            break
        bot_response = respond_to_user(user_input, user_data)
        print("בוט:", bot_response)










#עכשיו אני אבנה גרסה מתקדמת יותר של הבוט החכם בפייתון, שתכלול את כל המרכיבים העיקריים של המערכת שלך:
"""
ניהול קבוצות והפקת הצעות מחיר.
אימות זהות לפי אקסל.
Double Handshake – ניהול חברות בחדר.
איסוף העדפות ודירוג אישי.
חישוב מחיר כולל קופון או תשלום קבוצתי.
"""


# smart_bot.py
import pandas as pd

# -----------------------------
# נתונים לדוגמה
# -----------------------------
HOTELS = {
    "גלי צאנז": {"rooms": 10, "accessible": True},
    "גלי התמר": {"rooms": 5, "accessible": False}
}

COUPONS = {
    "WELCOME10": 10,
    "VIP50": 50
}

GROUPS_DB = {
    "קבוצת חן": ["0501234567", "0507654321"]
}

BOOKINGS = []

# -----------------------------
# פונקציות עזר
# -----------------------------
def load_group_excel(file_path):
    """טוען רשימת טלפונים של קבוצה מאקסל"""
    df = pd.read_excel(file_path)
    return df["phone"].tolist()

def is_valid_user(phone):
    """בודק אם המשתמש נמצא ברשימת המנהלת"""
    for group in GROUPS_DB.values():
        if phone in group:
            return True
    return False

def calculate_price(base_price, nights=1, coupon=None):
    price = base_price * nights
    if coupon and coupon in COUPONS:
        discount = COUPONS[coupon]
        price *= (1 - discount / 100)
    return price

# -----------------------------
# מנגנון Double Handshake
# -----------------------------
PENDING_FRIENDS = {}

def register_friend_request(user_phone, friend_phone):
    if friend_phone not in PENDING_FRIENDS:
        PENDING_FRIENDS[friend_phone] = []
    PENDING_FRIENDS[friend_phone].append(user_phone)
    return f"בקשה נשלחה ל-{friend_phone}. תהליך יאושר כאשר היא תענה."

def approve_friend(user_phone):
    if user_phone in PENDING_FRIENDS:
        approved = PENDING_FRIENDS[user_phone]
        del PENDING_FRIENDS[user_phone]
        return f"ידידות אושרה עם: {', '.join(approved)}"
    return "אין בקשות פתוחות עבורך."

# -----------------------------
# פונקציית התכתבות עיקרית
# -----------------------------
def respond_to_user(user_input, user_data):
    response = ""

    if "מסלול" in user_input:
        response += "אפשר לבחור בין מסלול פרימיום ליום אחד או מסלול בוטיק עם לינה.\n"

    elif "תאריך" in user_input:
        response += "יש לי נופשים בתאריכים: 11/07, 21/08. לאיזה מהם את מעוניינת?\n"

    elif "מלון" in user_input:
        hotel_name = [name for name in HOTELS.keys() if name in user_input]
        if hotel_name:
            hotel = hotel_name[0]
            rooms = HOTELS[hotel]["rooms"]
            response += f"יש לנו {rooms} חדרים פנויים ב-{hotel}.\n"
        else:
            response += "לא מצאתי את המלון שהזנת.\n"

    elif "החזרי לידה" in user_input:
        response += "יש לנו החזרי לידה, הפרטים מול המלון יש לבדוק ישירות.\n"

    elif "הסדר" in user_input:
        response += "אין לנו הסדר עם הספק שביקשת.\n"

    elif "מחיר" in user_input:
        base_price = 500
        coupon = None
        if "קופון" in user_input:
            words = user_input.split()
            for w in words:
                if w.upper() in COUPONS:
                    coupon = w.upper()
        price = calculate_price(base_price, nights=2, coupon=coupon)
        response += f"המחיר הכולל: {price} ש\"ח.\n"

    elif "נכה" in user_input or "מונגש" in user_input:
        response += "יש לנו חדרים מונגשים.\n"

    elif "חברה" in user_input:
        # דוגמה להזנת בקשת חברות
        words = user_input.split()
        if len(words) > 1:
            friend_phone = words[-1]
            response += register_friend_request(user_data["phone"], friend_phone)
        else:
            response += "אנא צייני מספר טלפון של החברה.\n"

    elif "מאשרת" in user_input:
        response += approve_friend(user_data["phone"])

    else:
        response += "לא הצלחתי להבין את הבקשה, אנא נסי שוב.\n"

    return response

# -----------------------------
# דוגמת שימוש
# -----------------------------
if __name__ == "__main__":
    user_data = {"phone": "0501234567"}
    while True:
        user_input = input("משתמש: ")
        if user_input.lower() in ["יציאה", "סיים"]:
            break
        bot_response = respond_to_user(user_input, user_data)
        print("בוט:", bot_response)









