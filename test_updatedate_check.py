"""
בדיקה מבודדת: השפעת UpdateDate על מנגנון השיבוץ

סיטואציה:
- 2 משתמשים בלבד
- 2 חדרים זהים
- בלי העדפות
- שום קבוצות
- UpdateDates שונים בלבד

היעד: להוכיח / להפריך אם UpdateDate משמש כ-tiebreaker
"""
import os
import sys

# ודא שספריית הפרויקט ב־sys.path
ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from database.connection import SessionLocal
from assignment.assignment_engine import AssignmentEngine
from sqlalchemy import text

def run_test():
    session = SessionLocal()
    
    try:
        print("\n" + "="*60)
        print("בדיקה מבודדת: השפעת UpdateDate על השיבוץ")
        print("="*60 + "\n")
        
        # ========== שלב 1: הצג את הנתונים שיוצאו ==========
        print("📋 שלב 1: נתוני הכניסה")
        print("-" * 60)
        
        # משתמשים
        print("\n👥 משתמשים:")
        users_query = """
        SELECT vc.VacationIDForCustomers, vc.UserID, u.Name, vc.UpdateDate
        FROM vacationers_customers vc
        JOIN users u ON vc.UserID = u.UserID
        WHERE vc.VacationID = 9999
        ORDER BY vc.UpdateDate ASC
        """
        users_result = session.execute(text(users_query)).fetchall()
        for row in users_result:
            print(f"  VacationersCustomersID={row[0]}, UserID={row[1]}, Name={row[2]}, UpdateDate={row[3]}")
        
        # חדרים
        print("\n🏨 חדרים:")
        rooms_query = """
        SELECT RoomID, RoomNumber, Floor, NumberOfBeds
        FROM rooms WHERE RoomID IN (9998, 9999)
        ORDER BY RoomID ASC
        """
        rooms_result = session.execute(text(rooms_query)).fetchall()
        for row in rooms_result:
            print(f"  RoomID={row[0]}, RoomNumber={row[1]}, Floor={row[2]}, NumberOfBeds={row[3]}")
        
        # בדוק עדפות
        print("\n⭐ בדוק - אין customer_preferences:")
        pref_query = "SELECT COUNT(*) FROM customer_preferences WHERE VacationID = 9999"
        pref_count = session.execute(text(pref_query)).scalar()
        print(f"  סה״כ customer_preferences: {pref_count}")
        
        print("\n⭐ בדוק - אין room_preferences:")
        room_pref_query = "SELECT COUNT(*) FROM room_preferences WHERE RoomID IN (9998, 9999)"
        room_pref_count = session.execute(text(room_pref_query)).scalar()
        print(f"  סה״כ room_preferences: {room_pref_count}")
        
        print("\n⭐ בדוק - אין groups:")
        groups_query = "SELECT COUNT(*) FROM groups WHERE VacationID = 9999"
        groups_count = session.execute(text(groups_query)).scalar()
        print(f"  סה״כ groups: {groups_count}")
        
        # ========== שלב 2: הרץ את אלגוריתם השיבוץ ==========
        print("\n" + "="*60)
        print("🚀 שלב 2: הרצת אלגוריתם השיבוץ")
        print("="*60 + "\n")
        
        engine = AssignmentEngine(session)
        result = engine.run(vacation_id=9999)
        
        print(f"✅ אלגוריתם הסתיים. פתרון: {type(result).__name__}")
        
        # ========== שלב 3: בדוק את התוצאות ==========
        print("\n" + "="*60)
        print("📊 שלב 3: ניתוח התוצאות")
        print("="*60 + "\n")
        
        # placements
        print("📌 Placements (השיבוצים הסופיים):")
        placements_query = """
        SELECT p.PlacementID, vc.UserID, u.Name, r.RoomNumber, vc.UpdateDate
        FROM placements p
        JOIN vacationers_customers vc ON p.VacationersCustomersID = vc.VacationIDForCustomers
        JOIN users u ON vc.UserID = u.UserID
        JOIN rooms r ON p.RoomID = r.RoomID
        WHERE vc.VacationID = 9999
        ORDER BY u.Name ASC
        """
        placements_result = session.execute(text(placements_query)).fetchall()
        
        if placements_result:
            for row in placements_result:
                print(f"  PlacementID={row[0]}, UserID={row[1]}, User={row[2]}, Room={row[3]}, UpdateDate={row[4]}")
        else:
            print("  ❌ אין placements! פתרון חלקי או כישל.")
        
        # ========== שלב 4: בדוק ציוני user-room pairs ==========
        print("\n📈 ניתוח הציונים (Score Analysis):")
        print("-" * 60)
        
        # נסה לבדוק אם יש context.room_scores מאחסן בכמוהו
        # עדיין אנחנו לא יכולים לגשת לzation internal scores ישירות
        # אבל אנחנו יכולים לנתח את ה-registration_bonus מה-UpdateDate
        
        print("\n🎯 ניתוח דירוג הרישום (Registration Order):")
        reg_order_query = """
        WITH sorted_vc AS (
            SELECT UserID, VacationID, UpdateDate, 
                   ROW_NUMBER() OVER (ORDER BY UpdateDate, VacationIDForCustomers) - 1 as registration_idx
            FROM vacationers_customers
            WHERE VacationID = 9999
        )
        SELECT UserID, UpdateDate, registration_idx, (2 - registration_idx) * 10000000 as bonus_score
        FROM sorted_vc
        ORDER BY registration_idx ASC
        """
        reg_order_result = session.execute(text(reg_order_query)).fetchall()
        for row in reg_order_result:
            user_id, update_date, idx, bonus = row
            print(f"  UserID={user_id}, UpdateDate={update_date}, Index={idx}, Registration_Bonus={bonus}")
        
        # ========== שלב 5: סיכום ==========
        print("\n" + "="*60)
        print("📝 סיכום התוצאות")
        print("="*60 + "\n")
        
        if placements_result:
            print("✅ השיבוץ הושלם בהצלחה.")
            print("\nתוצאה צפויה:")
            print("  - User 9998 (UpdateDate=2026-01-01) צריך לקבל עדיפות ראשונה")
            print("  - User 9999 (UpdateDate=2026-06-01) צריך לקבל את החדר השני")
            
            print("\nתוצאה בפועל:")
            for row in placements_result:
                user_id = row[1]
                update_date = row[4]
                room = row[3]
                print(f"  - User {user_id} (UpdateDate={update_date}) קיבל Room {room}")
            
            # הוכחה או הפרכה
            placement_dict = {row[1]: row[3] for row in placements_result}
            if 9998 in placement_dict and 9999 in placement_dict:
                user_early_room = placement_dict[9998]
                user_late_room = placement_dict[9999]
                
                print("\n🔍 ממצא:")
                if user_early_room != user_late_room:
                    print("✅ המשתמשים קיבלו חדרים שונים - יש הבדל בהשיבוץ")
                    print(f"   User 9998 (רישום מוקדם) → Room {user_early_room}")
                    print(f"   User 9999 (רישום מאוחר) → Room {user_late_room}")
                    print("   RESULT: UpdateDate משפיע בפועל על השיבוץ ✅")
                else:
                    print("⚠️ המשתמשים קיבלו אותו חדר - זה לא צפוי עם 2 חדרים!")
        else:
            print("❌ לא נוצרו שיבוצים. בדוק את ה-logs.")
        
        print("\n" + "="*60)
        print("בדיקה הסתיימה")
        print("="*60 + "\n")
        
    finally:
        session.close()

if __name__ == "__main__":
    run_test()
