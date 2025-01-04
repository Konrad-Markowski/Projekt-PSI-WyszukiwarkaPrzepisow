"""Module containing service implementation"""

from typing import Iterable

from src.core.domain.meal import Meal, MealBroker
from src.core.repositories.imeal import IMealRepository
from src.infrastructure.dto.mealdto import MealDTO
from src.infrastructure.services.imeal import IMealService


class MealService(IMealService):
    """A class implementing the meal service."""

    def __init__(self, repository: IMealRepository) -> None:
        """The initializer of the `meal service`.

        Args:
            repository (IMealRepository): The reference to the repository.
        """
        self._repository = repository

    async def get_all(self) -> Iterable[MealDTO]:
        """The method getting all meals from the repository.

        Returns:
            Iterable[MealDTO]: All meals.
        """
        return await self._repository.get_all_meals()

    async def get_by_id(self, meal_id: int) -> MealDTO | None:
        """The method getting meal by provided id.

        Args:
            meal_id (int): The id of the meal.

        Returns:
            MealDTO | None: The meal details.
        """
        return await self._repository.get_by_id(meal_id)

    async def get_by_category(self, category_id: int) -> Iterable[Meal]:
        """The method getting meals assigned to a particular category.

        Args:
            category_id (int): The id of the category.

        Returns:
            Iterable[Meal]: Meals assigned to a category.
        """
        return await self._repository.get_by_category(category_id)

    async def add_meal(self, data: MealBroker) -> Meal | None:
        """The method adding new meal to the data storage.

        Args:
            data (MealBroker): The details of the new meal.

        Returns:
            Meal | None: Full details of the newly added meal.
        """
        return await self._repository.add_meal(data)

    async def update_meal(self, meal_id: int, data: MealBroker) -> Meal | None:
        """The method updating meal data in the data storage.

        Args:
            meal_id (int): The id of the meal.
            data (MealBroker): The details of the updated meal.

        Returns:
            Meal | None: The updated meal details.
        """
        return await self._repository.update_meal(meal_id, data)

    async def delete_meal(self, meal_id: int) -> bool:
        """The method removing meal from the data storage.

        Args:
            meal_id (int): The id of the meal.

        Returns:
            bool: Success of the operation.
        """
        return await self._repository.delete_meal(meal_id)
