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

                variables[
                    (user.UserID, room.RoomID)
                ] = model.NewBoolVar(
                    f"user_{user.UserID}_room_{room.RoomID}"
                )

        return variables