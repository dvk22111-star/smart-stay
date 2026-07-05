class SatisfactionScoreCalculator:

    # ממיר דירוג להעדפה מספרית
    # עדיפות 1 גוברת באופן חד-משמעי על כל האפשרויות של עדיפות 2.
    def calculate_score(
        self,
        rating
    ):

        if rating is None:
            return 0

        weights = {
            1: 1000000,
            2: 10000,
            3: 100,
            4: 10,
            5: 1,
        }

        return weights.get(rating, 0)
