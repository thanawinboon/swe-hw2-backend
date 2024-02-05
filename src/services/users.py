from sqlmodel import select

from src.models.users import User
from src.services.base import BaseService


class UserService(BaseService):
    def create_user(self, user: User) -> User:
        """
        Inserts a new user into the database.
        :param user: The user object containing the user information.
        """
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)

        return user

    def get_user_by_username(self, username: str) -> User:
        """
        Queries the database for a user by their username.
        :param username: The username to query.
        :return: `User` corresponding to the username or `None` if no user with that
        username exists.
        """
        query = select(User).where(User.username == username)
        result = self.session.exec(query).one_or_none()

        return result

    def increment_remaining_leave_days(self, username: str, days: int) -> None:
        """
        Increment the specified amount of days to user's remaining leave days.
        :param username: The username of the user to query.
        :param days: The number of days to increment.
        """
        user: User = self.get_user_by_username(username)
        user.remaining_leave_days += days
        self.session.add(user)
        self.session.commit()

    def deduct_remaining_leave_days(self, username: str, days: int) -> None:
        """
        Deducts the specified amount of days from user's remaining leave days.
        :param username: The username of the user to query.
        :param days: The number of days to deduct.
        """
        user: User = self.get_user_by_username(username)
        user.remaining_leave_days -= days
        self.session.add(user)
        self.session.commit()

    def reset_remaining_leave_days(self, username: str) -> None:
        # should be ran by scheduler (e.g. cronjob)
        """
        Resets the remaining leave days of the user to 10.
        :param username: The username of the user to query.
        """
        user: User = self.get_user_by_username(username)
        user.remaining_leave_days = 10
        self.session.add(user)
        self.session.commit()

    def get_user_by_user_id(self, user_id: int) -> int:
        """
        Queries the database for a user by their id.
        :param username: The username to query.
        :return: `User` corresponding to the username or `None` if no user with that
        username exists.
        """
        query = select(User).where(User.id == user_id)
        result = self.session.exec(query).one_or_none()
        return result
