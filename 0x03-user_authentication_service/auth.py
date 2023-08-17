#!/usr/bin/env python3
"""
Authentication Module
"""

import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4

from typing import Union

def _hash_password(password: str) -> str:
    """Hashes a password using bcrypt.

    Args:
        password (str): The plaintext password.

    Returns:
        str: The hashed password.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def _generate_uuid() -> str:
    """Generates a UUID4 string.

    Returns:
        str: A UUID4 string.
    """
    id = uuid4()
    return str(id)

class Auth:
    """Authentication class for user authentication.
    """

    def __init__(self):
        """Initializes an instance of the Auth class.
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> Union[None, User]:
        """Registers a new user.

        Args:
            email (str): The user's email.
            password (str): The user's password.

        Returns:
            Union[None, User]: Returns None or the registered User object.
        """
        try:
            # Check if user with given email exists
            self._db.find_user_by(email=email)
        except NoResultFound:
            # Add user to database
            return self._db.add_user(email, _hash_password(password))
        else:
            # If user already exists, raise an error
            raise ValueError(f"User '{email}' already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """Validates a user's login credentials.

        Args:
            email (str): The user's email.
            password (str): The user's password.

        Returns:
            bool: True if the login is valid, False otherwise.
        """
        try:
            # Find user with the given email
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        # Check the validity of the password
        return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)

    # ... (Other methods follow with similar detailed comments)

