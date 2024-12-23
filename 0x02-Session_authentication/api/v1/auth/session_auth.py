#!/usr/bin/env python3
""" Session Authentication module."""
from api.v1.auth.auth import Auth
from typing import Dict, TypeVar
import uuid
from models.user import User


class SessionAuth(Auth):
    """ Class SessionAuth"""
    user_id_by_session_id: Dict = {}

    def create_session(self, user_id: str = None) -> str:
        """ creates a Session ID for a user_id."""
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Returns a User ID based on a Session ID."""
        if session_id is None or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> TypeVar('User'):
        """ Returns s User instance based on a cookie value."""
        session_id: str = self.session_cookie(request)
        user_id: str = self.user_id_for_session_id(session_id)
        user = User.get(user_id)

        return user

    def destroy_session(self, request=None):
        """ Deletes the session ID contains in the request as cookie. """
        if request is None:
            return False

        session_id: str = self.session_cookie(request)
        if session_id is None:
            return False

        if self.user_id_for_session_id(session_id) is None:
            return False

        del self.user_id_by_session_id[session_id]
        return True
