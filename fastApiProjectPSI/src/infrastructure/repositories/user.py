from typing import Any
from pydantic import UUID4
from src.infrastructure.utils.password import hash_password
from src.core.domain.user import UserIn
from src.core.repositories.iuser import IUserRepository
from src.db import database, user_table, meal_table



"""A repository for user entity."""


class UserRepository(IUserRepository):
    """An implementation of repository class for user."""

    async def register_user(self, user: UserIn) -> Any | None:
        """A method registering new user.

        Args:
            user (UserIn): The user input data.

        Returns:
            Any | None: The new user object.
        """

        if await self.get_by_email(user.email):
            return None

        user.password = hash_password(user.password)

        query = user_table.insert().values(**user.model_dump())
        new_user_uuid = await database.execute(query)

        return await self.get_by_uuid(new_user_uuid)

    async def get_by_uuid(self, uuid: UUID4) -> Any | None:
        """A method getting user by UUID.

        Args:
            uuid (UUID4): UUID of the user.

        Returns:
            Any | None: The user object if exists.
        """

        query = user_table \
            .select() \
            .where(user_table.c.id == uuid)
        user = await database.fetch_one(query)

        return user

    async def get_by_email(self, email: str) -> Any | None:
        """A method getting user by email.

        Args:
            email (str): The email of the user.

        Returns:
            Any | None: The user object if exists.
        """

        query = user_table \
            .select() \
            .where(user_table.c.email == email)
        user = await database.fetch_one(query)

        return user
    
    async def add_to_favourites(self, user_uuid: UUID4, meal_id: int) -> bool:
        """Add a meal to the user's favourites list based on the meal ID.

        Args:
            user_uuid (UUID4): The UUID of the user.
            meal_id (int): The ID of the meal to be added.

        Returns:
            bool: True if the meal was successfully added, False otherwise.
        """
  
        query = meal_table.select(). \
                where(meal_table.c.id == meal_id)
        meal = await database.fetch_one(query)

        if meal:
            meal_name = meal["strMeal"]

            query = user_table.select().where(user_table.c.id == user_uuid)
            user = await database.fetch_one(query)

            if user:
                current_favourites = user["favourites"] if "favourites" in user else []
                if meal_name not in current_favourites:
                    current_favourites.append(meal_name)

                    update_query = (
                        user_table.update()
                        .where(user_table.c.id == user_uuid)
                        .values(favourites=current_favourites)
                    )
                    await database.execute(update_query)
                    return True
        return False
    
    async def remove_from_favourites(self, user_uuid: UUID4, meal_id: int) -> bool:
        """Remove a meal from the user's favourites list based on the meal ID.

        Args:
            user_uuid (UUID4): The UUID of the user.
            meal_id (int): The ID of the meal to be removed.

        Returns:
            bool: True if the meal was successfully removed, False otherwise.
        """
        query = meal_table.select().where(meal_table.c.id == meal_id)
        meal = await database.fetch_one(query)

        if meal:
            meal_name = meal["strMeal"]

            query = user_table.select().where(user_table.c.id == user_uuid)
            user = await database.fetch_one(query)

            if user:
                current_favourites = user["favourites"] if "favourites" in user else []
                if meal_name in current_favourites:
                    current_favourites.remove(meal_name)

                    update_query = (
                        user_table.update()
                        .where(user_table.c.id == user_uuid)
                        .values(favourites=current_favourites)
                    )
                    await database.execute(update_query)
                    return True
        return False
    
    async def get_favourites(self, user_uuid: UUID4) -> list:
        """Get a user's favourite meals by their UUID.

        Args:
            user_uuid (UUID4): The UUID of the user.

        Returns:
            list: A list of favourite meal names.
        """
        query = user_table.select().where(user_table.c.id == user_uuid)
        user = await database.fetch_one(query)

        if user:
            return user["favourites"] if "favourites" in user else []
        return []
    
    async def get_all_users(self) -> list:
        """Retrieve all users.

        Returns:
            list: A list of all user objects.
        """
        query = user_table.select()
        users = await database.fetch_all(query)
        return users