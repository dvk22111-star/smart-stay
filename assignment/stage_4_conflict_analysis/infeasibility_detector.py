from ortools.sat.python import cp_model


class InfeasibilityDetector:

    # בודק האם המודל אינו פתיר
    def is_infeasible(
        self,
        status
    ):

        return status == cp_model.INFEASIBLE