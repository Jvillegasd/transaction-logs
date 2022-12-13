class UserNotFound(Exception):
    """Raises when an user is not found in database."""


class BadCredentials(Exception):
    """Raises when bad credentials like wrong password where provided"""
