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
    async def recommend_meals(user_id: UUID4, count: int = 5):
         """A method randomly selecting 5 meals and displaying them as a JSON file structure.

        Args:
            user_id (UUID4): The UUID of the user.
            count (int): The number of meals to recommend. Defaults to 5.

        Returns:
            List: A list of dictionaries containing user_id and meal_id pairs.
        """