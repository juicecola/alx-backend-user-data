#!/usr/bin/env python3
"""DB module for user data management.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB:
    """A class for interacting with the user database.
    """

    def __init__(self) -> None:
        """Initialize a new DB instance and create databasei
        tables if they don't exist.
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """A memoized session object to manage database operations.
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a new user to the database.

        Args:
            email (str): User's email address.
            hashed_password (str): Hashed user password.

        Returns:
            User: The created User object.
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """Find a user in the database based on specified criteria.

        Args:
            **kwargs: Keyword arguments representing search criteria.

        Returns:
            User: The found User object.

        Raises:
            InvalidRequestError: When no search criteria are provided.
            NoResultFound: When no user matches the provided criteria.
        """
        if not kwargs:
            raise InvalidRequestError("No search criteria provided.")

        user = self._session.query(User).filter_by(**kwargs).first()
        if not user:
            raise NoResultFound("No user found with the specified criteria.")
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update user information in the database.

        Args:
            user_id (int): ID of the user to update.
            **kwargs: Updated user attributes and values.

        Raises:
            ValueError: When an attribute provided in kwargs
            doesn't exist in the User class.
        """
        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError(f"User has no attribute '{key}'.")
            setattr(user, key, value)

        self._session.commit()
