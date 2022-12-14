from src.connection import get_dal
from src.services.users import UserService
from src.middlewares.auth import is_authenticated
from src.errors.users import BadCredentials, UserNotFound

from flask import Blueprint, request, abort, session

users_api = Blueprint('users', __name__)
user_service = UserService()


@users_api.post('/auth')
def auth_user():
    with get_dal().get_session() as db:
        try:
            data: dict = request.get_json()
            user_model = user_service.auth(data, db)
            user_serialized = user_model.serialize()
        except BadCredentials as e:
            abort(401, str(e))
        except UserNotFound as e:
            abort(404, str(e))

    return user_serialized


@users_api.get('/account-balance')
@is_authenticated
def account_balance():
    with get_dal().get_session() as db:
        user_id = session.get('user_id')
        balance: float = user_service.get_account_balance(user_id, db)

    return {'account_balance': balance}


@users_api.route('/logout')
@is_authenticated
def logout_user():
    return user_service.logout()
