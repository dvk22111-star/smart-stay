def build_report(assignments, total_users):
    """
    דו"ח סטטיסטי
    """
    assigned_users = len(assignments)
    unassigned_users = total_users - assigned_users
    return {
        "total_users": total_users,
        "assigned_users": assigned_users,
        "unassigned_users": unassigned_users
    }