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
        assignment_bonus
    ):
        # Combine room score and registration bonus into per-variable terms.
        # This guarantees the registration bonus affects tie-breaking
        # independently of variable ordering or IDs.
        objective_terms = []

        for user in users:

            user_bonus = assignment_bonus.get(user.UserID, 0)

            for room in rooms:
                score = room_scores.get((user.UserID, room.RoomID), 0)

                total_score = score + user_bonus

                if total_score:
                    objective_terms.append(
                        variables[(user.UserID, room.RoomID)] * total_score
                    )

        model.Maximize(sum(objective_terms))