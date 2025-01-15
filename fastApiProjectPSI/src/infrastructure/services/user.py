"""A module containing user service."""

from pydantic import UUID4

from src.core.domain.user import UserIn
from src.core.repositories.iuser import IUserRepository
from src.infrastructure.dto.userdto import UserDTO
from src.infrastructure.dto.tokendto import TokenDTO
from src.infrastructure.services.iuser import IUserService
from src.infrastructure.utils.password import verify_password
from src.infrastructure.utils.token import generate_user_token


class UserService(IUserService):
    """An abstract class for user service."""

    _repository: IUserRepository

    def __init__(self, repository: IUserRepository) -> None:
        self._repository = repository

    async def register_user(self, user: UserIn) -> UserDTO | None:
        """A method registering a new user.

        Args:
            user (UserIn): The user input data.

        Returns:
            UserDTO | None: The user DTO model.
        """

        return await self._repository.register_user(user)

    async def authenticate_user(self, user: UserIn) -> TokenDTO | None:
        """The method authenticating the user.

        Args:
            user (UserIn): The user data.

        Returns:
            TokenDTO | None: The token details.
        """

        if user_data := await self._repository.get_by_email(user.email):
            if verify_password(user.password, user_data.password):
                token_details = generate_user_token(user_data.id)
                # trunk-ignore(bandit/B106)
                return TokenDTO(token_type="Bearer", **token_details)

            return None

        return None

    async def get_by_uuid(self, uuid: UUID4) -> UserDTO | None:
        """A method getting user by UUID.

        Args:
            uuid (UUID4): The UUID of the user.

        Returns:
            UserDTO | None: The user data, if found.
        """

        return await self._repository.get_by_uuid(uuid)


    async def get_by_email(self, email: str) -> UserDTO | None:
        """A method getting user by email.

        Args:
            email (str): The email of the user.

        Returns:
            UserDTO | None: The user object if exists.
        """
        return await self._repository.get_by_email(email)
    

    async def add_to_favourites(self, user_uuid: UUID4, meal_id: int) -> bool:
        """Add a meal to the user's favourites.

        Args:
            user_uuid (UUID4): The UUID of the user.
            meal_id (int): The ID of the meal to be added.

        Returns:
            bool: True if added, False if not found or already exists.
        """
        return await self._repository.add_to_favourites(user_uuid, meal_id)

    async def remove_from_favourites(self, user_uuid: UUID4, meal_id: int) -> bool:
        """Remove a meal from the user's favourites by its ID.

        Args:
            user_uuid (UUID4): The UUID of the user.
            meal_id (int): The ID of the meal to be removed.

        Returns:
            bool: True if removed, False if not found in favourites.
        """
        return await self._repository.remove_from_favourites(user_uuid, meal_id)
    
    async def get_favourites(self, user_uuid: UUID4) -> list:
        """Get a user's favourite meals.

        Args:
            user_uuid (UUID4): The UUID of the user.

        Returns:
            list: A list of favourite meal names.
        """
        return await self._repository.get_favourites(user_uuid)