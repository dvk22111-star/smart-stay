from datetime import datetime
from assignment.stage_5_optimization.stage_5_service import Stage5OptimizationService
from assignment.stage_5_optimization.objective_builder import ObjectiveBuilder

class Simple:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

class DummyRoomScoreCalculator:
    def calculate(self, user_preferences, room_preferences, score_calculator):
        return 100

class DummyScoreCalculator:
    def calculate_score(self, rating):
        return 1


def run_case(case_name, vcs):
    print(f"--- {case_name} ---")
    users = [Simple(UserID=vc.UserID) for vc in vcs]
    rooms = [Simple(RoomID=101), Simple(RoomID=102)]

    class Ctx: pass
    context = Ctx()
    context.vacation_customers = vcs
    context.users = users
    context.rooms = rooms
    context.customer_preferences = []
    context.room_preferences = []
    context.model = None
    context.variables = {(u.UserID, r.RoomID): None for u in users for r in rooms}
    context.assigned_users = {}

    obj_builder = ObjectiveBuilder()
    svc = Stage5OptimizationService(score_calculator=DummyScoreCalculator(), room_score_calculator=DummyRoomScoreCalculator(), objective_builder=obj_builder)
    svc.execute(context)

    # recompute registration_order exactly as in code for clarity
    registration_order = {vc.UserID: idx for idx, vc in enumerate(sorted(context.vacation_customers, key=lambda vc: (vc.UpdateDate, vc.VacationIDForCustomers)))}
    total_users = len(context.users)
    base_weight = 10_000_000
    assignment_bonus = {}
    for user in context.users:
        registration_bonus = 0
        if user.UserID in registration_order:
            registration_bonus = (total_users - registration_order[user.UserID]) * base_weight
        assignment_bonus[user.UserID] = registration_bonus

    print('registration_order =', registration_order)
    print('assignment_bonus =', assignment_bonus)

    # room_scores were built in stage_5_service; recompute simple room_scores from builder
    # but objective_builder received room_scores; we can recompute same way
    from assignment.stage_5_optimization.room_score_calculator import RoomScoreCalculator
    rsc = RoomScoreCalculator()
    room_scores = {}
    for u in users:
        for r in rooms:
            room_scores[(u.UserID, r.RoomID)] = rsc.calculate([], [], DummyScoreCalculator())

    for u in users:
        total = room_scores[(u.UserID, 101)] + assignment_bonus[u.UserID]
        print(f'user {u.UserID} total for room 101 =', total)


if __name__ == '__main__':
    # Case A: Late has earlier UpdateDate
    vc_late = Simple(UserID=1, UpdateDate=datetime(2026,1,1), VacationIDForCustomers=1)
    vc_early = Simple(UserID=2, UpdateDate=datetime(2026,2,1), VacationIDForCustomers=2)
    run_case('Late earlier UpdateDate', [vc_late, vc_early])

    # Case B: swap dates
    vc_late2 = Simple(UserID=1, UpdateDate=datetime(2026,3,1), VacationIDForCustomers=1)
    vc_early2 = Simple(UserID=2, UpdateDate=datetime(2026,2,1), VacationIDForCustomers=2)
    run_case('Early earlier UpdateDate', [vc_late2, vc_early2])
