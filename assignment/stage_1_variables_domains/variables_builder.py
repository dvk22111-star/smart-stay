from ortools.sat.python import cp_model


class VariablesBuilder:

    # יוצר משתנה עבור כל צירוף:
    # משתמש × חדר
    #
    # x[(user_id, room_id)]
    #
    # המשתנה מייצג:
    # 1 = המשתמש שובץ בחדר
    # 0 = המשתמש לא שובץ בחדר
    def build(
        self,
        model: cp_model.CpModel,
        users,
        rooms
    ):

        variables = {}

        for user in users:
            for room in rooms:
                var_name = f"user_{user.UserID}_room_{room.RoomID}"
                variables[(user.UserID, room.RoomID)] = model.NewBoolVar(var_name)

        return variables


    def build_assigned_users(
        self,
        model: cp_model.CpModel,
        users
    ):

        assigned = {}

        for user in users:
            assigned[user.UserID] = model.NewBoolVar(
                f"user_{user.UserID}_assigned"
            )

        return assigned


    def build_room_usage_flags(
        self,
        model: cp_model.CpModel,
        rooms
    ):

        room_used = {}
        room_full = {}

        for room in rooms:
            room_used[room.RoomID] = model.NewBoolVar(
                f"room_{room.RoomID}_used"
            )
            room_full[room.RoomID] = model.NewBoolVar(
                f"room_{room.RoomID}_full"
            )

        return room_used, room_full