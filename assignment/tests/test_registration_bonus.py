from datetime import datetime

from assignment.stage_5_optimization.stage_5_service import Stage5OptimizationService


class DummyObjectiveBuilder:
    def __init__(self):
        self.received = None

    def build(self, model, variables, assigned_users, users, rooms, room_scores, assignment_bonus):
        # store for inspection in tests
        self.received = {
            "model": model,
            "variables": variables,
            "assigned_users": assigned_users,
            "users": users,
            "rooms": rooms,
            "room_scores": room_scores,
            "assignment_bonus": assignment_bonus,
        }


class DummyRoomScoreCalculator:
    def calculate(self, user_preferences, room_preferences, score_calculator):
        # return a constant score so tie depends solely on registration bonus
        return 100


class DummyScoreCalculator:
    def calculate_score(self, rating):
        return 1


class Simple:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


def test_registration_bonus_prioritizes_earlier_update_date():
    # Late has earlier UpdateDate, Early later UpdateDate
    late = Simple(UserID=1)
    early = Simple(UserID=2)

    vc_late = Simple(UserID=1, UpdateDate=datetime(2026, 1, 1), VacationIDForCustomers=1)
    vc_early = Simple(UserID=2, UpdateDate=datetime(2026, 2, 1), VacationIDForCustomers=2)

    users = [late, early]
    rooms = [Simple(RoomID=101), Simple(RoomID=102)]

    class Ctx:
        pass

    context = Ctx()
    context.vacation_customers = [vc_late, vc_early]
    context.users = users
    context.rooms = rooms
    context.customer_preferences = []
    context.room_preferences = []
    context.model = None
    context.variables = {(u.UserID, r.RoomID): None for u in users for r in rooms}
    context.assigned_users = {}

    obj_builder = DummyObjectiveBuilder()
    svc = Stage5OptimizationService(score_calculator=DummyScoreCalculator(), room_score_calculator=DummyRoomScoreCalculator(), objective_builder=obj_builder)

    svc.execute(context)

    assignment_bonus = obj_builder.received["assignment_bonus"]
    room_scores = obj_builder.received["room_scores"]

    # For two users the earlier UpdateDate (late) should get larger bonus
    assert assignment_bonus[1] > assignment_bonus[2]

    # total score for (user,room) should be room_score + assignment_bonus
    total_late = room_scores[(1, 101)] + assignment_bonus[1]
    total_early = room_scores[(2, 101)] + assignment_bonus[2]

    assert total_late > total_early
