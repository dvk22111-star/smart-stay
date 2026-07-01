from ortools.sat.python import cp_model


class ConstraintsBuilder:

    # מחזיר אילוצים ראשוניים למודל CP-SAT
    # כולל:
    # 1. כל משתמש מקבל בדיוק חדר אחד
    # 2. קיבולת חדר
    # 3. אילוצים ספציפיים של משתמש
    def apply(
        self,
        model: cp_model.CpModel,
        variables: dict,
        users: list,
        rooms: list,
        room_capacities: dict,
        user_constraints: dict
    ):

        # 1️⃣ כל משתמש מקבל בדיוק חדר אחד
        for user in users:

            user_vars = [
                variables[(user.UserID, room.RoomID)]
                for room in rooms
            ]

            model.AddExactlyOne(user_vars)

        # 2️⃣ קיבולת חדר
        for room in rooms:

            room_vars = [
                variables[(user.UserID, room.RoomID)]
                for user in users
            ]

            capacity = room_capacities.get(
                room.RoomID,
                room.NumberOfBeds
            )

            model.Add(
                sum(room_vars) <= capacity
            )

        # 3️⃣ אילוצי משתמש
        # user_constraints:
        # {
        #   user_id: [room_id, room_id, ...]
        # }
        for user_id, allowed_rooms in user_constraints.items():

            for room in rooms:

                if room.RoomID not in allowed_rooms:

                    model.Add(
                        variables[
                            (user_id, room.RoomID)
                        ] == 0
                    )