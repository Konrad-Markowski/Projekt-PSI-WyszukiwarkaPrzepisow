from typing import Any, Iterable, List

from pydantic import UUID4
import sqlalchemy
from asyncpg import Record  # type: ignore
from sqlalchemy import func, select

from src.core.repositories.imeal import IMealRepository
from src.core.domain.meal import Meal, MealBroker
from src.db import (
    meal_table,
    database,
)
from src.infrastructure.dto.mealdto import MealDTO


class MealRepository(IMealRepository):
    """A class representing meal DB repository."""
    
    async def get_all_meals(self) -> Iterable[Any]:
        """The method getting all meals from the data storage.

        Returns:
            Iterable[Any]: Meals in the data storage.
        """

        query = (
            select(meal_table)
            .order_by(meal_table.c.id.asc()) #strMeal jeśi chcemy sortować po nazwie
        )
        meals = await database.fetch_all(query)

        return [MealDTO.from_record(meal) for meal in meals]

    async def get_by_category(self, category: str) -> Iterable[Any]:
        """The method getting meals assigned to particular category.

        Args:
            category (str): The name of the category.

        Returns:
            Iterable[Any]: Meals assigned to a category.
        """

        query = meal_table \
        .select() \
        .where(func.lower(meal_table.c.strCategory) == category.lower()) \
        .order_by(meal_table.c.strMeal.asc())

        meals = await database.fetch_all(query)
        return [Meal(**dict(meal)) for meal in meals]

    async def get_by_ingredients(self, ingredient_name: str) -> List[MealDTO]:
        """The method getting meals containing a particular ingredient.

        Args:
            ingredient_name (str): The name of the ingredient.

        Returns:
            List[MealDTO]: Meals containing the specified ingredient.
        """

        query = select(meal_table).where(
            meal_table.c.ingredients.op('@>')([ingredient_name])
        ).order_by(meal_table.c.strMeal.asc())

        meals = await database.fetch_all(query)
        return [MealDTO.from_record(meal) for meal in meals]

    async def get_by_area(self, area: str) -> Iterable[Any]:
        """The method getting meals assigned to particular area.

        Args:
            area (str): The name of the area.

        Returns:
            Iterable[Any]: Meals assigned to an area.
        """

        query = meal_table \
        .select() \
        .where(func.lower(meal_table.c.strArea) == area.lower()) \
        .order_by(meal_table.c.strMeal.asc())

        meals = await database.fetch_all(query)
        return [Meal(**dict(meal)) for meal in meals]

    async def get_by_id(self, meal_id: int) -> Any | None:
        """The method getting meal by provided id.

        Args:
            meal_id (int): The id of the meal.

        Returns:
            Any | None: The meal details.
        """

        meal = await self._get_by_id(meal_id)

        return MealDTO.from_record(meal) if meal else None

    async def get_by_name(self, name: str) -> Iterable[Any]:
        """The method getting meals by their name.

        Args:
            name (str): The name of the meal.

        Returns:
            Iterable[Any]: Meals with the specified name.
        """

        query = meal_table \
        .select() \
        .where(meal_table.c.strMeal.ilike(f"%{name}%")) \
        .order_by(meal_table.c.strMeal.asc())

        meals = await database.fetch_all(query)
        return [Meal(**dict(meal)) for meal in meals]

    async def get_by_user(self, user_id: UUID4) -> Iterable[Any]:
        """The method getting meals by user who added them.

        Args:
            user_id (UUID4): The UUID of the user.

        Returns:
            Iterable[Any]: The meal collection.
        """
        query = meal_table \
            .select() \
            .where(meal_table.c.user_id == user_id) \
            .order_by(meal_table.c.strMeal.asc())

        meals = await database.fetch_all(query)
        return [MealDTO.from_record(meal) for meal in meals]

    async def add_meal(self, data: MealBroker) -> Any | None:
        """The method adding new meal to the data storage.

        Args:
            data (MealBroker): The details of the new meal.

        Returns:
            Any | None: The newly added meal.
        """

        query = meal_table.insert().values(**data.model_dump())
        new_meal_id = await database.execute(query)
        new_meal = await self._get_by_id(new_meal_id)

        return Meal(**dict(new_meal)) if new_meal else None

    async def update_meal(
        self,
        meal_id: int,
        data: MealBroker,
    ) -> Any | None:
        """The method updating meal data in the data storage.

        Args:
            meal_id (int): The id of the meal.
            data (MealBroker): The details of the updated meal.

        Returns:
            Any | None: The updated meal details.
        """

        if await self._get_by_id(meal_id):
            query = (
                meal_table.update()
                .where(meal_table.c.id == meal_id)
                .values(**data.model_dump())
            )
            await database.execute(query)

            meal = await self._get_by_id(meal_id)

            return Meal(**dict(meal)) if meal else None

        return None

    async def delete_meal(self, meal_id: int) -> bool:
        """The method removing meal from the data storage.

        Args:
            meal_id (int): The id of the meal.

        Returns:
            bool: Success of the operation.
        """

        if await self._get_by_id(meal_id):
            query = meal_table \
                .delete() \
                .where(meal_table.c.id == meal_id)
            await database.execute(query)

            return True

        return False

    async def _get_by_id(self, meal_id: int) -> Record | None:
        """A private method getting meal from the DB based on its ID.

        Args:
            meal_id (int): The ID of the meal.

        Returns:
            Any | None: Meal record if exists.
        """

        query = meal_table \
            .select() \
            .where(meal_table.c.id == meal_id) \
            .order_by(meal_table.c.strMeal.asc())

        return await database.fetch_one(query)

    async def recommend_meals(self, n: int = 3) -> List[dict]:
        """A coroutine to get random meal recommendations.

        Args:
            n (int, optional): The number of meals to recommend. Defaults to 3.

        Returns:
            List[dict]: A list of recommended meals as dictionaries.
        """
        query = select(meal_table).order_by(func.random()).limit(n)
        meals = await database.fetch_all(query)
        return [MealDTO.from_record(meal).model_dump() for meal in meals]