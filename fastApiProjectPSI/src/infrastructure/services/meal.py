"""Module containing service implementation"""

from typing import Iterable, List

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

    async def get_all_meals(self) -> Iterable[MealDTO]:
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
    
    async def recommend_meals(self, n: int = 3) -> List[dict]:
        """The method recommending random meals.

        Args:
            n (int, optional): The number of meals to recommend. Defaults to 3.

        Returns:
            List[dict]: A list of recommended meals as dictionaries.
        """
        recommendations = await self._repository.recommend_meals(n)
        return recommendations

    async def get_by_category(self, category_id: int) -> Iterable[Meal]:
        """The method getting meals assigned to a particular category.

        Args:
            category_id (int): The id of the category.

        Returns:
            Iterable[Meal]: Meals assigned to a category.
        """

        return await self._repository.get_by_category(category_id)

    async def get_by_area(self, area: str) -> Iterable[Meal]:
        """The method getting meals by area.

        Args:
            area (str): The area of the meals.

        Returns:
            Iterable[Meal]: Meals from the specified area.
        """

        return await self._repository.get_by_area(area)

    async def get_by_name(self, name: str) -> MealDTO | None:
        """The method getting meal by name.

        Args:
            name (str): The name of the meal.

        Returns:
            MealDTO | None: The meal details.
        """

        return await self._repository.get_by_name(name)
    
    async def get_by_user(self, user_id: int) -> Iterable[MealDTO]:
        """The method getting meals assigned to a particular user.

        Args:
            user_id (int): The id of the user.

        Returns:
            Iterable[MealDTO]: Meals assigned to the user.
        """

        return await self._repository.get_by_user(user_id)


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
    
    


    async def get_by_ingredients(self, ingredient_name: str) -> List[dict]:
        """The method getting meals by a specific ingredient.

        Args:
            ingredient_name (str): The name of the ingredient.

        Returns:
            List[dict]: Meals containing the specified ingredient.
        """
        return await self._repository.get_by_ingredients(ingredient_name)