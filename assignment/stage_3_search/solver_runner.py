from ortools.sat.python import cp_model


class SolverRunner:

    # מריץ את מנוע החיפוש
    def run(self, model):

        solver = cp_model.CpSolver()

        status = solver.Solve(model)

        return solver, status