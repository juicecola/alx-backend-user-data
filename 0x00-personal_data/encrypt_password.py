#!/usr/bin/env python3
"""
encrypt_password.py - Module for hashing and validating passwords using bcrypt.
"""

import bcrypt


def hash_password(password):
    """
    Hash and salt a password using bcrypt.

    Args:
        password (str): The password to be hashed.

    Returns:
        bytes: The hashed and salted password as bytes.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def is_valid(hashed_password, password):
    """
    Validate that the provided password matches the hashed password.

    Args:
        hashed_password (bytes): The hashed and salted password as bytes.
        password (str): The password to be validated.

    Returns:
        bool: True if the password matches the hashed password, False otherwise.
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)


if __name__ == "__main__":
    # Test the functions
    password = "MyAmazingPassw0rd"
    encrypted_password = hash_password(password)
    print(f"Hashed Password: {encrypted_password}")
    print(f"Password Validation: {is_valid(encrypted_password, password)}")

