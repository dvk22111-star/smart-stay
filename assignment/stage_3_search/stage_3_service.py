from ortools.sat.python import cp_model
from .search_strategy_builder import SearchStrategyBuilder
from .solver_configuration import SolverConfiguration


class Stage3SearchService:

    def __init__(self):
        self._strategy_builder = SearchStrategyBuilder()
        self._solver_config = SolverConfiguration()

    def execute(self, context):
        """
        מריץ את שלב החיפוש (Search)
        מחזיר solver + status
        """

        # 1️⃣ קביעת אסטרטגיית חיפוש (MRV וכו')
        self._strategy_builder.configure(
            context.model,
            context.variables
        )

        # 2️⃣ יצירת solver
        solver = cp_model.CpSolver()

        # 3️⃣ הגדרות ביצועים
        self._solver_config.configure(solver)

        # 4️⃣ הרצת פתרון
        status = solver.Solve(context.model)

        return solver, status