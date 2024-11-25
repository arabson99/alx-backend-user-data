#!/usr/bin/env python3
""" Session Authentication module."""
from api.v1.auth.auth import Auth
from typing import Dict, TypeVar
import uuid


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