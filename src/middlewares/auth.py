from typing import Callable
from functools import wraps

from flask import abort, session


def is_authorized(endpoint: Callable) -> Callable:

    @wraps(endpoint)
    def wrapper(*args, **kwargs):
        if 'user_id' in session:
            return endpoint(*args, **kwargs)
        else:
            abort(401, 'User is not logged in')

    return wrapper
