class SatisfactionScoreCalculator:
    WEIGHTS = {
        1: 10_000_000,
        2: 250_000,
        3: 2_500,
        4: 100,
        5: 10,
    }

    # ממיר דירוג להעדפה מספרית
    # עדיפות 1 גוברת באופן חד-משמעי על כל האפשרויות של עדיפות 2.
    def calculate_score(
        self,
        rating
    ):

        if rating is None:
            return 0

        return self.WEIGHTS.get(rating, 0)
