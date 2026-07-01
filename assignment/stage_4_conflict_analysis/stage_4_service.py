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

        statistics = (
            self.statistics_builder.build(
                solver
            )
        )

        report = (
            self.report_builder.build(
                status
            )
        )

        infeasible = (
            self.infeasibility_detector
            .is_infeasible(
                status
            )
        )

        return {
            "statistics": statistics,
            "report": report,
            "infeasible": infeasible
        }