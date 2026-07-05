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
        user_constraints: dict,
        partner_requests: list
    ):

        # 1️⃣ כל משתמש מקבל בדיוק חדר אחד
        # לפי ההנחה שאין יותר משתמשים ממיטות, כל המשתמשים חייבים להשתבץ.
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

        # 4️⃣ בקשות שותפים: שני משתמשים בבקשת שותפות חייבים לקבל את אותו חדר
        # או להישאר ללא שיבוץ, כדי לאפשר פתרונות חלקיים.
        for request in partner_requests:
            u1 = request.UserIDMember1
            u2 = request.UserIDMember2
            if u1 is None or u2 is None:
                continue

            for room in rooms:
                model.Add(
                    variables[(u1, room.RoomID)] == variables[(u2, room.RoomID)]
                )