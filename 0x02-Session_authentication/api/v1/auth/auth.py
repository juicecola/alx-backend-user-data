#!/usr/bin/env python3
"""
Module for authentication
"""


from typing import List, TypeVar
from flask import request
import os


class Auth:
    """A class for handling authentication methods.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Check if authentication is required for the given path.

        Args:
            path (str): The requested path.
            excluded_paths (List[str]): List of paths to be excluded from authentication.

        Returns:
            bool: True if authentication is required, False otherwise.
        """
        if path is None:
            return True

        if excluded_paths is None or excluded_paths == []:
            return True

        if path in excluded_paths:
            return False

        for excluded_path in excluded_paths:
            if excluded_path.startswith(path):
                return False
            elif path.startswith(excluded_path):
                return False
            elif excluded_path[-1] == "*":
                if path.startswith(excluded_path[:-1]):
                    return False

        return True

    def authorization_header(self, request=None) -> str:
        """Get the authorization header from the request.

        Args:
            request (_type_, optional): The Flask request object. Defaults to None.

        Returns:
            str: The authorization header value.
        """
        if request is None:
            return None
        # Get header from the request
        header = request.headers.get('Authorization')

        if header is None:
            return None

        return header

    def current_user(self, request=None) -> TypeVar('User'):
        """Get the current user from the request.

        Args:
            request (_type_, optional): The Flask request object. Defaults to None.

        Returns:
            TypeVar('User'): The current user.
        """

        return None

    def session_cookie(self, request=None):
        """Get the session cookie from the request.

        Args:
            request (_type_, optional): The Flask request object. Defaults to None.
        """
        if request is None:
            return None
        session_name = os.getenv('SESSION_NAME')
        return request.cookies.get(session_name)

