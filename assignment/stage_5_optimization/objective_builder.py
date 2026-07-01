from ortools.sat.python import cp_model


class ObjectiveBuilder:

    def build(
        self,
        model,
        variables,
        users,
        rooms,
        room_scores
    ):

        objective_terms = []

        for user in users:

            for room in rooms:

                score = room_scores.get(
                    (user.UserID, room.RoomID),
                    0
                )

                objective_terms.append(
                    variables[
                        (
                            user.UserID,
                            room.RoomID
                        )
                    ] * score
                )

        model.Maximize(
            sum(objective_terms)
        )