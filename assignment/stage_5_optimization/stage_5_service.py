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

        # בניית דירוג רישום על בסיס תאריך עדכון,
        # כך שאם אין מקום לכולם יתקבל פתרון שמעדיף משתמשים שנרשמו קודם.
        registration_order = {
            vc.UserID: idx
            for idx, vc in enumerate(
                sorted(
                    context.vacation_customers,
                    key=lambda vc: (vc.UpdateDate, vc.VacationIDForCustomers)#VacationersCustomersID)
                )
            )
        }
        max_registration_rank = max(registration_order.values(), default=-1)

        for user in context.users:

            user_preferences = [

                p

                for p in context.customer_preferences

                if p.UserID == user.UserID

            ]

            registration_bonus = 0
            if user.UserID in registration_order:
                registration_bonus = (
                    max_registration_rank - registration_order[user.UserID]
                ) * 20

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

                # נשתמש ברישום בלבד כשובר שוויון, לא כדי להחליף העדפה.
                room_scores[
                    (
                        user.UserID,
                        room.RoomID
                    )
                ] = score + registration_bonus

        self.objective_builder.build(
            context.model,
            context.variables,
            context.users,
            context.rooms,
            room_scores
        )

        return context