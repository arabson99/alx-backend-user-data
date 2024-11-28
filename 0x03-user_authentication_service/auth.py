#!/usr/bin/env python3
""" auth module. """

import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError


def _hash_password(password: str) -> str:
    """ Hashes a password and return the hashed password."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self) -> None:
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Regiater a user"""

        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists.")
        except NoResultFound:
            password: str = _hash_password(password).decode('utf-8')
            user = self._db.add_user(email, password)

        return user
