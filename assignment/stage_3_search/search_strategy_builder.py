from ortools.sat.python import cp_model


class SearchStrategyBuilder:

    # מגדיר ל-CP-SAT באיזה סדר לבחור משתנים
    def configure(
        self,
        model,
        variables
    ):

        model.AddDecisionStrategy(
            list(variables.values()),
            cp_model.CHOOSE_MIN_DOMAIN_SIZE,
            cp_model.SELECT_MIN_VALUE
        )