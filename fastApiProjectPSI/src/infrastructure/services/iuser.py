"""A module containing user service."""


from abc import ABC, abstractmethod

from pydantic import UUID4

from src.core.domain.user import UserIn
from src.infrastructure.dto.userdto import UserDTO
from src.infrastructure.dto.tokendto import TokenDTO


class IUserService(ABC):
    """An abstract class for user service."""

    @abstractmethod
    async def register_user(self, user: UserIn) -> UserDTO | None:
        """A method registering a new user.

        Args:
            user (UserIn): The user input data.

        Returns:
            UserDTO | None: The user DTO model.
        """

    @abstractmethod
    async def authenticate_user(self, user: UserIn) -> TokenDTO | None:
        """The method authenticating the user.

        Args:
            user (UserIn): The user data.

        Returns:
            TokenDTO | None: The token details.
        """

    @abstractmethod
    async def get_by_uuid(self, uuid: UUID4) -> UserDTO | None:
        """A method getting user by UUID.

        Args:
            uuid (UUID4): The UUID of the user.

        Returns:
            UserDTO | None: The user data, if found.
        """

    @abstractmethod
    async def get_by_email(self, email: str) -> UserDTO | None:
        """A method getting user by email.

        Args:
            email (str): The email of the user.

        Returns:
            UserDTO | None: The user data, if found.
        """
    
    @abstractmethod
    async def add_to_favourites(self, uuid: UUID4, meal_id: int) -> UserDTO | None:
        """A method to add a meal to the user's favourites.

        Args:
            uuid (UUID4): The UUID of the user.
            meal_id (int): The ID of the meal to add.

        Returns:
            UserDTO | None: The updated user DTO if successful.
        """
        
    @abstractmethod
    async def remove_from_favourites(self, uuid: UUID4, meal_id: int) -> bool:
        """A method to remove a meal from the user's favourites.

        Args:
             uuid (UUID4): The UUID of the user.
             meal_id (int): The ID of the meal to remove.

        Returns:
            bool: True if the meal was successfully removed, False otherwise.
        """
        
    @abstractmethod
    async def get_favourites(self, uuid: UUID4) -> list:
        """A method to get the user's favourite meals.

        Args:
            uuid (UUID4): The UUID of the user.

        Returns:
            list: A list of favourite meal names.
        """

    @abstractmethod
    async def get_all_users(self) -> list[UserDTO]:
        """A method to get all users.

        Returns:
            list[UserDTO]: A list of all user DTOs.
        """