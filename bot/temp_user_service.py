class TempUserService:
    def __init__(self):
        self._users = {}

    def save(self, session_id: str, data: dict):
        self._users[session_id] = data

    def update(self, session_id: str, key: str, value):
        if session_id not in self._users:
            self._users[session_id] = {}

        self._users[session_id][key] = value

    def get(self, session_id: str):
        return self._users.get(session_id)

    def delete(self, session_id: str):
        self._users.pop(session_id, None)


temp_user_service = TempUserService()