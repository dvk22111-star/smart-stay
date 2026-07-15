from ortools.sat.python import cp_model


class ObjectiveBuilder:

    def build(
        self,
        model,
        variables,
        assigned_users,
        users,
        rooms,
        room_scores,
        assignment_bonus,
        group_room_bonus=None,
        partner_requests=None,
        room_used=None,
        room_full=None,
        max_room_score=0
    ):
        # Combine room score and registration bonus into per-variable terms.
        # This guarantees the registration bonus affects tie-breaking
        # independently of variable ordering or IDs.
        objective_terms = []

        for user in users:

            user_bonus = assignment_bonus.get(user.UserID, 0)

            for room in rooms:
                score = room_scores.get((user.UserID, room.RoomID), 0)
                group_bonus = group_room_bonus.get((user.UserID, room.RoomID), 0) if group_room_bonus else 0

                priority_multiplier = 1 + (user_bonus // 10_000_000)
                total_score = (score + group_bonus) * priority_multiplier + user_bonus

                var = variables[(user.UserID, room.RoomID)]

                if total_score:
                    objective_terms.append(
                        var * total_score
                    )

        # 2️⃣ העדפת בקשות שותפים כ־soft constraints.
        # אם שני המשתתפים משובצים לאותו חדר, הם מקבלים בונוס חזק.
        # אם לא — אין פסילה, רק אין בונוס.
        partner_bonus = max_room_score * 3 + 2
        group_priority_bonus = max_room_score * 2 + 1
        partner_term_count = 0

        if partner_requests:
            for req in partner_requests:
                u1 = getattr(req, 'UserIDMember1', None)
                u2 = getattr(req, 'UserIDMember2', None)
                if u1 is None or u2 is None:
                    continue

                for room in rooms:
                    y_name = f"partner_{u1}_{u2}_room_{room.RoomID}"
                    y = model.NewBoolVar(y_name)

                    x1 = variables.get((u1, room.RoomID))
                    x2 = variables.get((u2, room.RoomID))
                    if x1 is None or x2 is None:
                        continue

                    model.Add(y <= x1)
                    model.Add(y <= x2)
                    model.Add(y >= x1 + x2 - 1)

                    objective_terms.append(y * partner_bonus)
                    partner_term_count += 1

        if room_used:
            for room in rooms:
                used_var = room_used.get(room.RoomID)
                if used_var is not None:
                    objective_terms.append(used_var * -10_000)

        if room_full:
            for room in rooms:
                full_var = room_full.get(room.RoomID)
                if full_var is not None:
                    objective_terms.append(full_var * 1_000)

        model.Maximize(sum(objective_terms))