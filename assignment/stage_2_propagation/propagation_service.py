# assignment/stage_2_propagation/stage2_propagation_service.py

from ortools.sat.python import cp_model
from assignment.stage_2_propagation.constraints_builder import ConstraintsBuilder
from assignment.stage_2_propagation.build_user_domains import build_user_domains
from assignment.stage_1_variables_domains.assignment_context import AssignmentContext


class Stage2PropagationService:

    def __init__(self):
        self._constraints_builder = ConstraintsBuilder()

    # מבצע Propagation
    # מקבל AssignmentContext משלב 1 ומחזיר אותו עם אילוצים ראשוניים
    def execute(self, context: AssignmentContext) -> AssignmentContext:

        # 1️⃣ בניית אילוצי משתמשים לפי דומיינים
        user_constraints = build_user_domains(
            context.users,
            context.rooms,
            context.customer_preferences,
            context.room_preferences
        )

        # 2️⃣ יצירת מפת קיבולת חדרים
        room_capacities = {
            room.RoomID: room.NumberOfBeds
            for room in context.rooms
        }

        # 3️⃣ החלת האילוצים במודל CP-SAT
        self._constraints_builder.apply(
            model=context.model,
            variables=context.variables,
            users=context.users,
            rooms=context.rooms,
            room_capacities=room_capacities,
            user_constraints=user_constraints,
            partner_requests=context.partner_requests
        )

        # 4️⃣ החזרת Context עם האילוצים שהתווספו
        return context