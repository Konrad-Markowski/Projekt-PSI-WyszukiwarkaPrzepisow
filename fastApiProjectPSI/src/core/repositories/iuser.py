from abc import ABC, abstractmethod
from typing import Any

from pydantic import UUID4

from src.core.domain.user import UserIn


class IUserRepository(ABC):
    """An abstract repository class for user."""

    @abstractmethod
    async def register_user(self, user: UserIn) -> Any | None:
        """A method registering new user.

        Args:
            user (UserIn): The user input data.

        Returns:
            Any | None: The new user object.
        """

    @abstractmethod
    async def get_by_uuid(self, uuid: UUID4) -> Any | None:
        """A method getting user by UUID.

        Args:
            uuid (UUID4): UUID of the user.

        Returns:
            Any | None: The user object if exists.
        """

    @abstractmethod
    async def get_by_email(self, email: str) -> Any | None:
        """A method getting user by email.

        Args:
            email (str): The email of the user.

        Returns:
            Any | None: The user object if exists.
        """

    @abstractmethod
    async def add_to_favourites(self, uuid: UUID4, meal_name: str) -> Any | None:
        """A method to add a meal name to the user's favourites.

        Args:
            uuid (UUID4): The UUID of the user.
            meal_name (str): The name of the meal to add.

        Returns:
            Any | None: The updated user object if successful.
        """

    @abstractmethod
    async def remove_from_favourites(self, uuid: UUID4, meal_id: UUID4) -> bool:
        """A method to remove a meal by its ID from the user's favourites.

        Args:
            uuid (UUID4): The UUID of the user.
            meal_id (UUID4): The ID of the meal to remove.

        Returns:
            bool: True if the meal was successfully removed, False otherwise.
        """

    @abstractmethod
    async def get_favourites(self, uuid: UUID4) -> Any | None:
        """A method to get the user's favourites.

        Args:
            uuid (UUID4): The UUID of the user.

        Returns:
            Any | None: The user's favourites.
        """

    @abstractmethod
    async def get_all_users(self) -> list[Any] | None:
        """A method to retrieve all users.

        Returns:
            list[Any] | None: A list of user objects if any exist.
        """