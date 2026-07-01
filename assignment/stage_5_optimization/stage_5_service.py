class Stage5OptimizationService:

    def __init__(
        self,
        score_calculator,
        room_score_calculator,
        objective_builder
    ):

        self.score_calculator = (
            score_calculator
        )

        self.room_score_calculator = (
            room_score_calculator
        )

        self.objective_builder = (
            objective_builder
        )

    def execute(
        self,
        context
    ):

        room_scores = {}

        for user in context.users:

            user_preferences = [

                p

                for p in context.customer_preferences

                if p.UserID == user.UserID

            ]

            for room in context.rooms:

                room_preferences = [

                    rp.IDPreferences

                    for rp in context.room_preferences

                    if rp.RoomID == room.RoomID

                ]

                score = (
                    self.room_score_calculator
                    .calculate(
                        user_preferences,
                        room_preferences,
                        self.score_calculator
                    )
                )

                room_scores[
                    (
                        user.UserID,
                        room.RoomID
                    )
                ] = score

        self.objective_builder.build(
            context.model,
            context.variables,
            context.users,
            context.rooms,
            room_scores
        )

        return context