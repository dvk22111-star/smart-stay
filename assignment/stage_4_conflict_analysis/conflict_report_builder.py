from ortools.sat.python import cp_model


class ConflictReportBuilder:

    # בונה דו"ח מצב הריצה
    def build(
        self,
        status
    ):

        if status == cp_model.OPTIMAL:
            return "נמצא פתרון אופטימלי"

        if status == cp_model.FEASIBLE:
            return "נמצא פתרון חוקי"

        if status == cp_model.INFEASIBLE:
            return "לא קיים פתרון חוקי"

        return "מצב לא ידוע"