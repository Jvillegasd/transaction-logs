from src.models.user import User
from src.schemas.filters import FilterSchema
from src.repositories.users import UserRepository
from src.errors.users import UserNotFound, BadCredentials

from flask import session
from sqlalchemy.orm.session import Session


class UserService:

    def __init__(self):
        self._repo = UserRepository(User)

    def auth(self, email: str, password: str, db: Session) -> User:
        """Authenticate a user by fetching in database their
        email and password.

        Args:
            -   email: str
            -   password: str
            -   db: Session

        Returns:
            -   User = User record of provided credentials.
        """

        filters = [
            FilterSchema(
                field_name='email',
                operation='eq',
                value=email
            )
        ]
        user_model = self._repo.find_one(db, filters)
        if not user_model:
            raise UserNotFound('User not found in database')

        if user_model.password != password:
            raise BadCredentials('Password is wrong')

        session['user_id'] = user_model.id
        return user_model

    def logout(self) -> dict:
        session.pop('user_id', None)
        return {'message': 'logged out'}
