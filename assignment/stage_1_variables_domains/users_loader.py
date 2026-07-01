# אחראי על שליפת כל הנרשמות לנופש מהמערכת

class UsersLoader:

    def __init__(self, vacationers_customers_repository):
        self._vacationers_customers_repository = (
            vacationers_customers_repository
        )

    # מחזיר את כל המשתמשות של הנופש
    def load(self, vacation_id):

        vacationers = (
            self._vacationers_customers_repository
            .get_by_vacation_id(vacation_id)
        )

        users = []

        for vacationer in vacationers:
            users.append(vacationer.user)

        return users