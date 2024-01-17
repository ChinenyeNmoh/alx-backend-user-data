#!/usr/bin/env python3
""" Module named session_auth to the class Auth """

from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar
import uuid


class SessionAuth(Auth):
    """ Class sessionAuth empty """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """that creates a Session ID for a user_id
        """
        if (user_id is None or
                type(user_id) is not str):
            return None
        sess_id = str(uuid.uuid4())
        self.user_id_by_session_id[sess_id] = user_id
        return sess_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """that returns a User ID based on a Session ID"""
        if (session_id is None or
                type(session_id) is not str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """ returns a User instance based on a cookie value """
        session_cookie = self.session_cookie(request)
        if session_cookie is None:
            return None
        _id = self.user_id_for_session_id(session_cookie)
        return User.get(_id)

    def destroy_session(self, request=None):
        """deletes the user session / logout"""
        if request is None:
            return False
        sess_id = self.session_cookie(request)
        if not sess_id:
            return False
        user_id = self.user_id_for_session_id(sess_id)
        if not user_id:
            return False
        else:
            del self.user_id_by_session_id[sess_id]
            return True
