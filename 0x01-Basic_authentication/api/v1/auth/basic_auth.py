#!/usr/bin/env python3
"""
Module for authentication using Basic auth
"""

from typing import TypeVar
from api.v1.auth.auth import Auth
import base64

from models.user import User

class BasicAuth(Auth):
    """
    Basic Authentication class, extends Auth class
    """

    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """
        Extract the base64 encoded portion of the Authorization header.

        Args:
            authorization_header (str): The full Authorization header.

        Returns:
            str: The extracted base64 encoded token.
        """
        if authorization_header is None or not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None

        token = authorization_header.split(' ')[-1]
        return token

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """
        Decode the base64 encoded authorization header.

        Args:
            base64_authorization_header (str): The base64 encoded authorization header.

        Returns:
            str: The decoded header.
        """
        if base64_authorization_header is None or not isinstance(base64_authorization_header, str):
            return None

        try:
            item_to_decode = base64_authorization_header.encode('utf-8')
            decoded = base64.b64decode(item_to_decode)
            return decoded.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):
        """
        Extract user credentials from the decoded authorization header.

        Args:
            decoded_base64_authorization_header (str): The decoded base64 authorization header.

        Returns:
            tuple: A tuple containing the extracted email and password.
        """
        if decoded_base64_authorization_header is None or not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)

        email, password = decoded_base64_authorization_header.split(':')
        return (email, password)

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        Get a user object based on email and password credentials.

        Args:
            user_email (str): The user's email.
            user_pwd (str): The user's password.

        Returns:
            TypeVar('User'): The user object if valid credentials, otherwise None.
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        try:
            users = User.search({"email": user_email})
            if not users or users == []:
                return None
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
            return None
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Get the current user based on the provided request.

        Args:
            request: The Flask request object (optional).

        Returns:
            TypeVar('User'): The current user object if valid, otherwise None.
        """
        auth_header = self.authorization_header(request)
        if auth_header is not None:
            token = self.extract_base64_authorization_header(auth_header)
            if token is not None:
                decoded = self.decode_base64_authorization_header(token)
                if decoded is not None:
                    email, password = self.extract_user_credentials(decoded)
                    if email is not None:
                        return self.user_object_from_credentials(email, password)

        return None

