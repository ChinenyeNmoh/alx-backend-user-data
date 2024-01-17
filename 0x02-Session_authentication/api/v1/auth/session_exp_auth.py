#!/usr/bin/env python3
"""Module that inherits from session_auth"""

from api.v1.auth.session_auth import SessionAuth
from models.user import User
import os
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """Class that inherits from SessionAuth"""

    def __init__(self):
        """Init method"""
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION'))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """Create a Session ID"""
        try:
            session_id = super().create_session(user_id)
        except Exception:
            return None
        session_dictionary = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Returns user id"""
        if session_id is None:
            return None
        _id = self.user_id_by_session_id.get(session_id)
        if not _id:
            return None
        if self.session_duration <= 0:
            return _id.get('user_id')
        created_at = _id.get('created_at')
        if not created_at:
            return None
        expire_time = created_at + timedelta(seconds=self.session_duration)
        if expire_time < datetime.now():
            return None
        else:
            return _id.get('user_id')
