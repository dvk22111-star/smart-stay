class Stage4Service:

    def __init__(
        self,
        statistics_builder,
        report_builder,
        infeasibility_detector
    ):

        self.statistics_builder = (
            statistics_builder
        )

        self.report_builder = (
            report_builder
        )

        self.infeasibility_detector = (
            infeasibility_detector
        )

    # מפיק נתוני קונפליקטים וסטטיסטיקות
    def execute(
        self,
        solver,
        status
    ) -> dict:

        statistics = self.statistics_builder.build(solver)

        # include solver objective metrics when available
        try:
            objective_value = solver.ObjectiveValue()
        except Exception:
            objective_value = None

        try:
            best_bound = solver.BestObjectiveBound()
        except Exception:
            best_bound = None

        report = self.report_builder.build(status)

        infeasible = (
            self.infeasibility_detector
            .is_infeasible(
                status
            )
        )

        return {
            "statistics": statistics,
            "objective_value": objective_value,
            "best_bound": best_bound,
            "report": report,
            "infeasible": infeasible
        }