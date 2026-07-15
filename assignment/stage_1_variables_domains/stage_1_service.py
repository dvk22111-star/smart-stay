from ortools.sat.python import cp_model
from assignment.stage_1_variables_domains.assignment_context import AssignmentContext
from assignment.stage_1_variables_domains.users_loader import UsersLoader
from assignment.stage_1_variables_domains.rooms_loader import RoomsLoader
from assignment.stage_1_variables_domains.variables_builder import VariablesBuilder
from models import HotelPreferences, VacationersCustomers, Vacation

# פונקציה לטעינת כל הנתונים מהמסד
from assignment.stage_1_variables_domains.load_vacation_data import load_vacation_data


class Stage1VariablesAndDomainsService:

    def __init__(self, vacationers_customers_repository, room_repository, session):
        self._users_loader = UsersLoader(vacationers_customers_repository)
        self._rooms_loader = RoomsLoader(room_repository)
        self._variables_builder = VariablesBuilder()
        self._session = session

    def execute(self, vacation_id, hotel_id):
        # 1️⃣ שליפת משתמשים וחדרים
        users = self._users_loader.load(vacation_id)
        rooms = self._rooms_loader.load(hotel_id)

        # 2️⃣ טעינת יתר הנתונים מהמסד
        data = load_vacation_data(self._session, vacation_id, hotel_id)

        customer_preferences = data["customer_prefs"]
        room_preferences = data["room_prefs"]
        partner_requests = data["partner_requests"]
        groups = data["groups"]
        group_members = data["group_members"]

        # טעינת טבלאות נוספות
        hotel_preferences = self._session.query(HotelPreferences).filter(HotelPreferences.HotelID == hotel_id).all()
        vacation_customers = self._session.query(VacationersCustomers).filter(VacationersCustomers.VacationID == vacation_id).all()
        vacation = self._session.query(Vacation).filter(Vacation.VacationID == vacation_id).one_or_none()

        # 3️⃣ יצירת מודל CP-SAT ומשתני השיבוץ
        model = cp_model.CpModel()
        variables = self._variables_builder.build(model, users, rooms)
        assigned_users = self._variables_builder.build_assigned_users(model, users)
        room_used, room_full = self._variables_builder.build_room_usage_flags(model, rooms)

        # 4️⃣ החזרת AssignmentContext מלא
        return AssignmentContext(
            model=model,
            users=users,
            rooms=rooms,
            variables=variables,
            assigned_users=assigned_users,
            room_used=room_used,
            room_full=room_full,
            customer_preferences=customer_preferences,
            room_preferences=room_preferences,
            hotel_preferences=hotel_preferences,
            partner_requests=partner_requests,
            groups=groups,
            group_members=group_members,
            vacation_customers=vacation_customers,
            vacation=vacation
        )