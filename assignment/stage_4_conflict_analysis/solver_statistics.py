class SolverStatistics:

    # מחזיר סטטיסטיקות על הריצה
    def build(self, solver):

        return {
            "branches": solver.NumBranches(),
            "conflicts": solver.NumConflicts(),
            "wall_time": solver.WallTime()
        }