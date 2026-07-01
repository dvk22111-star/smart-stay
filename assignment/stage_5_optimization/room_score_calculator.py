class RoomScoreCalculator:

    def calculate(
        self,
        user_preferences,
        room_preferences,
        score_calculator
    ):

        score = 0

        for preference in user_preferences:

            if (
                preference.PreferencesID
                in room_preferences
            ):

                score += (
                    score_calculator
                    .calculate_score(
                        preference.Rating
                    )
                )

        return score