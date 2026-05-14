#אלגוריתם שיבוץ ראשוני



from typing import List, Dict
from models.room import Room
from models.user import User
from models.partner_request import PartnerRequest
from models.customer_preferences import CustomerPreference


def assign_rooms(
        users: List[User],
        rooms: List[Room],
        partner_requests: List[PartnerRequest],
        customer_preferences: List[CustomerPreference]
) -> Dict[str, List[str]]:
    """
    מחזיר dict: room_id -> רשימת user_id שהוקצו לחדר
    """
    room_assignments: Dict[str, List[str]] = {room.room_id: [] for room in rooms}
    unassigned_users = {u.user_id for u in users}

    # מיפוי מהיר של בקשות שותפים
    partner_map = {}
    for pr in partner_requests:
        partner_map[pr.member1_id] = pr.member2_id
        partner_map[pr.member2_id] = pr.member1_id

    # שיבוץ זוגות קודם
    for user_id, partner_id in partner_map.items():
        if user_id in unassigned_users and partner_id in unassigned_users:
            for room in rooms:
                if room.number_of_beds - len(room_assignments[room.room_id]) >= 2:
                    room_assignments[room.room_id].extend([user_id, partner_id])
                    unassigned_users.remove(user_id)
                    unassigned_users.remove(partner_id)
                    break

    # סידור יתר המשתמשים לפי דירוג העדפות (נמוך = טוב יותר)
    pref_map = {}
    for cp in customer_preferences:
        pref_map.setdefault(cp.user_id, []).append(cp)

    # ממיינים לפי דירוג העדפות
    sorted_users = sorted(unassigned_users, key=lambda u_id: min(
        [cp.rating for cp in pref_map.get(u_id, [CustomerPreference(None, 10, u_id, None, None)])]))

    # שיבוץ המשתמשים לפי חדר פנוי
    for user_id in sorted_users:
        for room in rooms:
            if len(room_assignments[room.room_id]) < room.number_of_beds:
                room_assignments[room.room_id].append(user_id)
                break

    return room_assignments







#אלגוריתם שיבוץ משולב


def full_optimal_assignment_with_paid_partners(
        users: list,
        rooms: list,
        partner_requests: list,
        customer_preferences: list,
        groups: list,
        all_group_members: list
) -> dict[str, list[str]]:
    """
    אלגוריתם שיבוץ:
    - משתמשים ששילמו בלבד
    - קבוצות ששולמו או חלקי תשלום לפי טלפון
    - בקשות שותפים רק למי ששילם
    - מקסום שביעות רצון אישית
    """
    from collections import defaultdict

    # מיפוי מספרי טלפון של מי ששילם
    paid_phones = {u.phone for u in users if getattr(u, "paid", True)}

    # מיפוי התחלי של שיבוצים
    room_assignments = {room.room_id: [] for room in rooms}
    unassigned_users = {u.user_id for u in users if u.phone in paid_phones}

    # מיפוי מהיר של בקשות שותפים (רק למי ששילם)
    partner_map = {}
    for pr in partner_requests:
        member1_paid = any(u.user_id == pr.member1_id and u.phone in paid_phones for u in users)
        member2_paid = any(u.user_id == pr.member2_id and u.phone in paid_phones for u in users)
        if member1_paid and member2_paid:
            partner_map[pr.member1_id] = pr.member2_id
            partner_map[pr.member2_id] = pr.member1_id

    # פונקציה לחישוב שביעות רצון
    def satisfaction_score(room, users_in_room, customer_preferences):
        score = 0
        for user_id in users_in_room:
            prefs = [cp for cp in customer_preferences if cp.user_id == user_id]
            for pref in prefs:
                score += max(10 - pref.rating, 0)
        return score

    # קודם: שיבוץ קבוצות ששולמו כקבוצה או חלקי תשלום
    for group in groups:
        group_members = get_group_members(group.group_id, all_group_members)

        # אם הקבוצה לא שולמה כקבוצה, נשאיר רק מי ששילם
        if not group.paid_as_group:
            group_members = [u for u in group_members if u.phone in paid_phones]

        if not group_members:
            continue

        # מילוי חדרים לפי מספר מיטות
        idx = 0
        for room in rooms:
            available_beds = room.number_of_beds - len(room_assignments[room.room_id])
            if available_beds > 0:
                to_assign = group_members[idx: idx + available_beds]
                room_assignments[room.room_id].extend(to_assign)
                idx += len(to_assign)
                for u in to_assign:
                    if u.user_id in unassigned_users:
                        unassigned_users.remove(u.user_id)
            if idx >= len(group_members):
                break

        # אופטימיזציה פנימית בתוך החדרים של הקבוצה
        for room in rooms:
            members_in_room = [u for u in room_assignments[room.room_id] if u.user_id not in unassigned_users]
            if len(members_in_room) > 1:
                members_in_room.sort(
                    key=lambda uid: sum(10 - cp.rating for cp in customer_preferences if cp.user_id == uid),
                    reverse=True
                )
                room_assignments[room.room_id] = members_in_room

    # שיבוץ זוגות עם בקשות שותפים (רק למי ששילם)
    for user_id, partner_id in partner_map.items():
        if user_id in unassigned_users and partner_id in unassigned_users:
            for room in rooms:
                if room.number_of_beds - len(room_assignments[room.room_id]) >= 2:
                    room_assignments[room.room_id].extend([user_id, partner_id])
                    unassigned_users.remove(user_id)
                    unassigned_users.remove(partner_id)
                    break

    # שיבוץ יתר המשתמשים לפי מקסום שביעות רצון
    for user_id in list(unassigned_users):
        best_room = None
        best_score = -1
        for room in rooms:
            if len(room_assignments[room.room_id]) < room.number_of_beds:
                temp_users = room_assignments[room.room_id] + [user_id]
                score = satisfaction_score(room, temp_users, customer_preferences)
                if score > best_score:
                    best_score = score
                    best_room = room.room_id
        if best_room:
            room_assignments[best_room].append(user_id)
            unassigned_users.remove(user_id)

    return room_assignments


#פונקצית עזר: קבלת חברי קבוצה

def get_group_members(group_id: str, all_group_members: list) -> list[str]:
    return [member.user_id for member in all_group_members if member.group_id == group_id]



#פונקציה עזר: ציון שביעות רצון לחדר

def satisfaction_score(room: Room, users_in_room: list[str], customer_preferences: list[CustomerPreference]) -> int:
    score = 0
    for user_id in users_in_room:
        prefs = [cp for cp in customer_preferences if cp.user_id == user_id]
        for cp in prefs:
            score += max(0, 10 - cp.rating)  # דירוג נמוך = העדפה גבוהה
    return score






#חישוב ציון שביעות רצון לחדר

def satisfaction_score(room: Room, users_in_room: List[str], customer_preferences: List[CustomerPreference]) -> int:
    """
    מחשב ציון שביעות רצון של חדר לפי ההעדפות של המשתמשים שבו
    """
    score = 0
    for user_id in users_in_room:
        prefs = [cp for cp in customer_preferences if cp.user_id == user_id]
        for cp in prefs:
            # דירוג נמוך = העדפה גבוהה יותר -> נספור הפוך
            score += max(0, 10 - cp.rating)  # 10 = ציון מקסימום להעדפה הכי גבוהה
    return score
