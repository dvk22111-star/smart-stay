# service/assignment_service.py
from typing import List, Dict
from model.user import User
from model.room import Room
from model.group import Group
from model.customer_preference import CustomerPreference
from model.partner_request import PartnerRequest

def get_group_members(group_id: str, all_group_members: list) -> list[str]:
    return [member.user_id for member in all_group_members if member.group_id == group_id]

def satisfaction_score(room, users_in_room, customer_preferences):
    score = 0
    for user_id in users_in_room:
        prefs = [cp for cp in customer_preferences if cp.user_id == user_id]
        for pref in prefs:
            score += max(10 - pref.rating, 0)  # דירוג נמוך = רצוי יותר
    return score

def full_optimal_assignment(
    users: List[User],
    rooms: List[Room],
    partner_requests: List[PartnerRequest],
    customer_preferences: List[CustomerPreference],
    groups: List[Group],
    all_group_members: list
) -> Dict[str, List[str]]:

    room_assignments = {room.room_id: [] for room in rooms}
    unassigned_users = set(u.user_id for u in users)

    # מיפוי מהיר של בקשות שותפים
    partner_map = {pr.member1_id: pr.member2_id for pr in partner_requests}
    partner_map.update({pr.member2_id: pr.member1_id for pr in partner_requests})

    # קודם: שיבוץ קבוצות ששולמו כקבוצה
    for group in groups:
        if group.paid_as_group:
            group_members = [u for u in get_group_members(group.group_id, all_group_members) if u in unassigned_users]
            room_index = 0
            while group_members:
                room = rooms[room_index % len(rooms)]
                available_beds = room.number_of_beds - len(room_assignments[room.room_id])
                if available_beds > 0:
                    assign_count = min(len(group_members), available_beds)
                    to_assign = group_members[:assign_count]
                    room_assignments[room.room_id].extend(to_assign)
                    for u in to_assign:
                        unassigned_users.remove(u)
                    group_members = group_members[assign_count:]
                room_index += 1

            # אופטימיזציה פנימית בחדרים של הקבוצה
            for room in rooms:
                members_in_room = [u for u in room_assignments[room.room_id] if u not in unassigned_users]
                if len(members_in_room) > 1:
                    members_in_room.sort(
                        key=lambda uid: sum(10 - cp.rating for cp in customer_preferences if cp.user_id == uid),
                        reverse=True
                    )
                    room_assignments[room.room_id] = members_in_room

    # שיבוץ בקשות שותפים
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