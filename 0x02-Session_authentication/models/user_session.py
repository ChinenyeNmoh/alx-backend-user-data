#!/usr/bin/env python3
"""User_session module"""
from models.base import Base


class UserSession(Base):
    """Inherits from Base"""
    def __init__(self, *args: list, **kwargs: dict):
        """Initialize a UserSession instance"""
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.created_at = kwargs.get('created_at')
