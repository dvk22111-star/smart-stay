from ortools.sat.python import cp_model


class SearchResult:

    # בודק האם נמצא פתרון
    def is_success(
        self,
        status
    ):

        return status in (
            cp_model.FEASIBLE,
            cp_model.OPTIMAL
        )