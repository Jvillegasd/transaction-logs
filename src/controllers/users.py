from src import get_dal
from src.services.users import UserService

from flask import Blueprint, request

users_api = Blueprint('users', __name__)
user_service = UserService()


@users_api.post('/auth')
def auth_user():
    with get_dal().get_session() as db:
        data: dict = request.get_json()
        user_model = user_service.auth(data, db)

    return user_model


@users_api.route('/logout')
def logout_user():
    return user_service.logout()
