class SolverConfiguration:

    # הגדרות ביצועים של הסולבר
    def configure(self, solver):

        solver.parameters.num_search_workers = 8

        solver.parameters.max_time_in_seconds = 300

        solver.parameters.log_search_progress = True