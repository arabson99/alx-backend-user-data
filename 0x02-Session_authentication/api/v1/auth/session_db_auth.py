#!/usr/bin/env python3
""" Session database auth """

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """ Session DB auth class."""

    def create_session(self, user_id: str = None) -> str:
        """ Create a session and store it in the database."""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Retrieve the user ID based on the session ID from the database"""
        if session_id is None:
            return None
        UserSession.load_from_file()
        user_session = UserSession.search({'session_id': session_id})

        if not user_session:
            return None

        user = user_session[0]
        if user is None:
            return None

        expired_at = user.created_at + \
            timedelta(seconds=self.session_duration)

        if expired_at < datetime.now():
            return None
        return user.user_id

    def destroy_session(self, request=None):
        """ Destroy the auth session"""
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return False

        session_user = UserSession.search({'session_id': session_id})
        if not session_user:
            return False

        try:
            session_user[0].remove()
            UserSession.save_to_file()
        except Exception:
            return False

        return True
