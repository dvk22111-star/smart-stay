
from repositories.room_preferences_repository import RoomPreferencesRepository
from models.room_preferences import RoomPreferences

class RoomPreferencesService:
    def __init__(self, repo: RoomPreferencesRepository):
        self.repo = repo

    def create_room_preference(self, room_id, preference_id):
        room_pref = RoomPreferences(
            room_id=room_id,
            preference_id=preference_id
        )
        return self.repo.add(room_pref)

    def get_all_room_preferences(self):
        return self.repo.list_all()
