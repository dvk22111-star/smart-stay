
from repositories.preferences_repository import PreferencesRepository
from models.preferences import Preferences, PreferenceTypeEnum

class PreferencesService:
    def __init__(self, repo: PreferencesRepository):
        self.repo = repo

    def create_preference(self, preference_type: PreferenceTypeEnum):
        preference = Preferences(preference_type=preference_type)
        return self.repo.add(preference)

    def get_all_preferences(self):
        return self.repo.list_all()
