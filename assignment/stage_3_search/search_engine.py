# stage_3_search/search_engine.py

from copy import deepcopy

# בדיקה אם ניתן להקצות משתמש לחדר
def is_assignment_valid(user_id, room_id, assignment, room_capacities):
    current_users = assignment.get(room_id, [])
    capacity = room_capacities.get(room_id, 1)

    if len(current_users) >= capacity:
        return False

    return True

# מנוע חיפוש חכם עם MRV
def assign_users(users, user_domains, room_capacities):
    """
    users: רשימת אובייקטי משתמשים או dict עם user_id
    user_domains: {user_id: [room_id, room_id, ...]}
    room_capacities: {room_id: capacity}
    """
    assignment = {room_id: [] for room_id in room_capacities.keys()}

    # מיון משתמשים לפי MRV - הכי מעט חדרים אפשריים
    users_sorted = sorted(
        users,
        key=lambda user: len(user_domains.get(user.UserID, []))
    )

    # nogoods: רשימת קומבינציות (user_idx, room_id) שכבר נבדקו והובילו לכישלון
    nogoods = set()

    def backtrack(idx):
        if idx >= len(users_sorted):
            return True

        user = users_sorted[idx]
        user_id = user.UserID
        possible_rooms = user_domains.get(user_id, [])
        for room_id in possible_rooms:
            # בדוק אם הצירוף הזה מורכב מנוגוד ידוע
            if (idx, room_id, tuple(sorted((r for r in assignment if assignment[r])))) in nogoods:
                continue
            if is_assignment_valid(user_id, room_id, assignment, room_capacities):
                assignment[room_id].append(user_id)
                if backtrack(idx + 1):
                    return True
                # ביטול הקצאה
                assignment[room_id].remove(user_id)

        # רישום nogood בסיסי: אם כל האפשרויות נכשלו עבור idx, נסמן את המצב הנוכחי כnogood
        nogoods.add((idx, None, tuple(sorted((r for r in assignment if assignment[r])))))

        return False

    success = backtrack(0)
    if not success:
        return None

    return assignment