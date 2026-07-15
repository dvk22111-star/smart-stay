def extract_solution(model_vars, solver):
    """
    מקבל את כל המשתנים x[user_id, room_id] ואת ה-solver
    מחזיר dict של user_id -> room_id שהוקצו
    """
    assignments = {}

    for (user_id, room_id), var in sorted(model_vars.items()):
        if solver.Value(var) == 1:
            assignments[user_id] = room_id

    return assignments