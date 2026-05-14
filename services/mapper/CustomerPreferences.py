

from repositories.customer_preferences_repository import CustomerPreferencesRepository
from models.customer_preferences import CustomerPreferences

class CustomerPreferencesService:
    def __init__(self, repo: CustomerPreferencesRepository):
        self.repo = repo

    def create_customer_preference(self, rating, user_id, preferences_id, vacation_id):
        customer_pref = CustomerPreferences(
            rating=rating,
            user_id=user_id,
            preferences_id=preferences_id,
            vacation_id=vacation_id
        )
        return self.repo.add(customer_pref)

    def get_all_customer_preferences(self):
        return self.repo.list_all()
