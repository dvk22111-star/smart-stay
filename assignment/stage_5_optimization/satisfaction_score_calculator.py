class SatisfactionScoreCalculator:

    # ממיר דירוג להעדפה מספרית
    def calculate_score(
        self,
        rating
    ):

        if rating == 1:
            return 100

        if rating == 2:
            return 50

        if rating == 3:
            return 25

        return 0