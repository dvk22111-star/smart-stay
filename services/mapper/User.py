


from repositories.user_repository import UserRepository
from models.user import User

class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def create_user(self, name, phone, email, credit=0.0):
        user = User(name=name, phone=phone, email=email, credit=credit)
        return self.repo.add(user)

    def get_all_users(self):
        return self.repo.list_all()

