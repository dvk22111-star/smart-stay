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
        assignment_bonus = {}

        # בניית דירוג רישום על בסיס תאריך עדכון,
        # כך שאם אין מקום לכולם יתקבל פתרון שמעדיף משתמשים שנרשמו קודם.
        registration_order = {
            vc.UserID: idx
            for idx, vc in enumerate(
                sorted(
                    context.vacation_customers,
                    key=lambda vc: (vc.UpdateDate, vc.VacationIDForCustomers)
                )
            )
        }

        total_users = len(context.users)
        base_weight = 10_000_000

        for user in context.users:

            user_preferences = [
                p
                for p in context.customer_preferences
                if p.UserID == user.UserID
            ]

            registration_bonus = 0
            if user.UserID in registration_order:
                registration_bonus = (
                    total_users - registration_order[user.UserID]
                ) * base_weight

            assignment_bonus[user.UserID] = registration_bonus

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
            context.assigned_users,
            context.users,
            context.rooms,
            room_scores,
            assignment_bonus
        )

        return context