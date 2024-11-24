#!/usr/bin/env python3
"""
    Auth Class
"""
    
from flask import request
from typing import List, TypeVar

class Auth:
    """ A class to manage the API authentication"""
    
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Returns False - path and excluded_paths"""
        if path is None or not excluded_paths or len(excluded_paths) == 0:
            return True
        if not path.endswith('/'):
            path += '/'
            
        normalized_excluded_paths = [ep if ep.endswith('/') else ep + '/' for ep in excluded_paths]
        
        for ep in normalized_excluded_paths:
            if ep.endswith('*'):
                prefix =ep[:-1]
                if path.startswith(prefix):
                    return False
            elif path == ep:
                return False
        return True
    
    def authorization_header(self, request=None) -> str:
        """ Returns None - request """
        if request is None or "Authorization" not in request.headers:
            return None
        return request.headers.get('Authorization')
    
    def current_user(self, request=None) -> TypeVar('User'):
        """ Returns None - request """
        return None