
from repositories.hotel_preferences_repository import HotelPreferencesRepository
from models.hotel_preferences import HotelPreferences

class HotelPreferencesService:
    def __init__(self, repo: HotelPreferencesRepository):
        self.repo = repo

    def create_hotel_preference(self, hotel_id, preference_id, price):
        hotel_pref = HotelPreferences(
            hotel_id=hotel_id,
            preference_id=preference_id,
            price=price
        )
        return self.repo.add(hotel_pref)

    def get_all_hotel_preferences(self):
        return self.repo.list_all()
