from src.models.user import User
from src.repositories.users import UserRepository

from sqlalchemy.orm.session import Session


class UserService:

    def __init__(self):
        self._repo = UserRepository(User)

    def auth(self, email: str, password: str, db: Session) -> User:
        user_model = self._repo.find_by_id()