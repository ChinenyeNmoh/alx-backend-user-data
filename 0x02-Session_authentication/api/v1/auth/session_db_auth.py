#!/usr/bin/env python3
"""
Sessions in database
"""
from datetime import datetime, timedelta
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """Sessions in database"""

    def create_session(self, user_id=None):
        """creates and stores new instance of UserSession"""
        session_id = super().create_session(user_id)

        if session_id is None:
            return None

        kwargs = {"user_id": user_id, "session_id": session_id}
        user_session = UserSession(**kwargs)
        user_session.save()
        UserSession.save_to_file()

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """searches for and returns the User ID in the database"""
        if session_id is None:
            return None

        UserSession.load_from_file()
        user_session = UserSession.search({
            "session_id": session_id
        })
        if not user_session:
            return None

        user_session = user_session[0]
        expiry = user_session.created_at + \
            timedelta(seconds=self.session_duration)
        if expiry < datetime.utcnow():
            return None
        return user_session.user_id

    def destroy_session(self, request=None):
        """destroys the User Session based on teh session ID"""
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        user_id = self.user_id_for_session_id(session_id)

        if not user_id:
            return False

        user_session = UserSession.search({
            'session_id': session_id
        })

        if not user_session:
            return False

        user_session = user_session[0]

        try:
            user_session.remove()
            UserSession.save_to_file()
        except Exception:
            return False

        return True
