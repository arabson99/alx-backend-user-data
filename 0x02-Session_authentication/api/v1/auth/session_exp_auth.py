#!/usr/bin/env python3
""" Session Expiration Auth."""

from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
from os import getenv
from typing import Dict


class SessionExpAuth(SessionAuth):
    """ Class SessionExpAuth. """

    def __init__(self):
        """ Initialize a class."""
        try:
            self.session_duration = int(getenv('SESSION_DURATION', 0))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id: str = None) -> str:
        """ Creates a session ID"""
        session_id = super().create_session(user_id)
        if not session_id:
            return None

        session_decitonary: Dict = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_decitonary

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Retrieves the user_id associated with a session ID."""
        if session_id is None or session_id not in self.user_id_by_session_id:
            return None

        session_dictionary = self.user_id_by_session_id.get(session_id)
        if self.session_duration <= 0 or session_dictionary is None:
            return session_dictionary.get('user_id', None)

        created_at = session_dictionary.get('created_at', None)
        if 'created_at' not in session_dictionary:
            return None

        expired_at = created_at + timedelta(seconds=self.session_duration)
        if expired_at < datetime.now():
            return None

        return session_dictionary.get('user_id', None)
