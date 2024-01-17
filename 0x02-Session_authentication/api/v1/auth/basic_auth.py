#!/usr/bin/env python3
""" Module named basic_auth to the class Auth """

from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar
from base64 import b64decode


class BasicAuth(Auth):
    """ Class BasicAuth empty """

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """ Method that returns the Base64 part of the Authorization
            header for Basic Authentication
        """
        if authorization_header is None or \
                type(authorization_header) is not str:
            return None
        substring_slice = authorization_header[0:6]
        if substring_slice != 'Basic ':
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """Method in the class BasicAuth that returns the decoded value
           of a Base64 string base64_authorization_header
        """
        if (base64_authorization_header is None or
                type(base64_authorization_header) is not str):
            return None
        try:
            return b64decode(base64_authorization_header).decode('utf-8')
        except Exception as e:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """Method in the class BasicAuth that returns the user email and
           password from the Base64 decoded value.
        """
        if (
            decoded_base64_authorization_header is None
            or type(decoded_base64_authorization_header) is not str
        ):
            return (None, None)
        if (':' not in decoded_base64_authorization_header):
            return (None, None)
        u_name, p_wd = decoded_base64_authorization_header.split(':', 1)
        return (u_name, p_wd)

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """ Method in the class BasicAuth that returns the User instance based
            on his email and password.
        """
        if user_email is None or type(user_email) is not str:
            return None
        if user_pwd is None or type(user_pwd) is not str:
            return None
        if User.count() != 0:
            users_found = User.search({'email': user_email})
            if users_found:
                for user in users_found:
                    if user.is_valid_password(user_pwd):
                        return user
                # Move this line outside the loop
                return None
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """_summary_
        """
        auth_header = self.authorization_header(request)
        if auth_header is not None:
            token = self.extract_base64_authorization_header(auth_header)
            if token is not None:
                decoded = self.decode_base64_authorization_header(token)
                if decoded is not None:
                    email, password = self.extract_user_credentials(decoded)
                    if email is not None:
                        return self.user_object_from_credentials(
                            email, password)

        return
