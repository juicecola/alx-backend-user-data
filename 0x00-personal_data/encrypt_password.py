#!/usr/bin/env python3
"""
Encrypting passwords using bcrypt library.
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hash the password using bcrypt.

    Args:
        password: The plaintext password to be hashed.

    Returns:
        bytes: The hashed and salted password as bytes.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Check if the provided password matches the hashed password.

    Args:
        hashed_password: The hashed password as bytes.
        password: The plaintext password to be checked.

    Returns:
        bool: True if the provided password matches the hashed password, False otherwise.
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

