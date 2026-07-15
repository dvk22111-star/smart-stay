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
        assigned_users: dict,
        room_used_flags: dict,
        room_full_flags: dict,
        users: list,
        rooms: list,
        room_capacities: dict,
        user_constraints: dict,
        partner_requests: list
    ):

        # 1️⃣ כל משתמש מקבל חדר אחד או אפס בהתאם לקיבולת הכוללת
        # אם סך כל המיטות מספיק לכל המשתמשים -> נחייב כל משתמש להיות משובץ בדיוק בחדר אחד.
        total_capacity = sum(room_capacities.values()) if room_capacities else 0
        require_full_assignment = (total_capacity >= len(users))

        for user in users:

            user_vars = [
                variables[(user.UserID, room.RoomID)]
                for room in rooms
            ]

            if require_full_assignment:
                # Force each user to be assigned to exactly one room
                model.Add(sum(user_vars) == 1)
                # Mirror into the assigned_users flag for reporting
                if user.UserID in assigned_users:
                    model.Add(assigned_users[user.UserID] == 1)
            else:
                # Allow users to be unassigned when capacity is insufficient
                model.Add(sum(user_vars) <= 1)
                model.Add(sum(user_vars) == assigned_users[user.UserID])

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

            room_used = room_used_flags.get(room.RoomID) if room_used_flags else None
            room_full = room_full_flags.get(room.RoomID) if room_full_flags else None
            if room_used is not None:
                model.Add(sum(room_vars) >= 1).OnlyEnforceIf(room_used)
                model.Add(sum(room_vars) == 0).OnlyEnforceIf(room_used.Not())
            if room_full is not None:
                if capacity > 0:
                    model.Add(sum(room_vars) == capacity).OnlyEnforceIf(room_full)
                    model.Add(sum(room_vars) <= capacity - 1).OnlyEnforceIf(room_full.Not())
                else:
                    model.Add(room_full == 0)

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

        # 4️⃣ בקשות שותפים: אינן נאכפות כאן כ-Hard constraints.
        # בקשות השותפים יחוזקו בשלב האופטימיזציה בלבד,
        # אך לא יגרמו לידי פתרון חסר או בלתי אפשרי.
        pass
