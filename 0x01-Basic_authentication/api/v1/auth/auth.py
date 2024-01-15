#!/usr/bin/env python3
"""
Authentication file
"""

from flask import request
from typing import TypeVar, List


class Auth():
    """ Authentication call declaration
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ A public method of class Auth
        """
        if path is None or excluded_paths is None or excluded_paths == []:
            return True
        if path in excluded_paths or path + '/' in excluded_paths:
            return False
        for e in excluded_paths:
            if (path[:e.find('*')] in e[:e.find('*')]):
                return False
        else:
            return True

    def authorization_header(self, request=None) -> str:
        """ Another public method to check authorization header
        """
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """ Current User request method
        """
        return None
