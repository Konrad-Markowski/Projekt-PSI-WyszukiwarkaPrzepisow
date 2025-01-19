"""Module containing meal service abstractions."""

from abc import ABC, abstractmethod
from typing import Any, Iterable, Optional, List

from src.core.domain.meal import Meal, MealBroker
from src.infrastructure.dto.mealdto import MealDTO


class IMealService(ABC):
    """A class representing meal repository"""

    @abstractmethod
    async def get_all_meals(self) -> Iterable[Any]:
        """
        The abstract method for getting all meals from the database.

        Args:
            None.

        Returns:
            Iterable[Any]
        """

    @abstractmethod
    async def get_by_id(self, meal_id: int) -> Optional[Any]:
        """The abstract method for getting a meal recipe by provided id.

        Args:
            meal_id (int): The id of the meal.

        Returns:
            Any | None: The meal details available.
        """

    @abstractmethod
    async def get_by_name(self, meal_name: str) -> Iterable[Any]:
        """The abstract method for getting a meal recipe by provided meal name.

        Args:
            meal_name (str): The name of the meal.

        Returns:
            Iterable[Any]: The meal details available.
        """

    @abstractmethod
    async def get_by_category(self, meal_category: str) -> Iterable[Any]:
        """The abstract method for getting a meal recipe by provided meal category.

        Args:
            meal_category (str): The category of the meal.

        Returns:
            Iterable[Any]: The meal details available.
        """

    @abstractmethod
    async def get_by_user(self, user_id: int) -> Iterable[Any]:
        """The abstract method for getting meals by a specific user.

        Args:
            user_id (int): The ID of the user.

        Returns:
            Iterable[Any]: The meal details associated with the user.
        """


    @abstractmethod
    async def recommend_meals(self, n: int = 3) -> List[dict]:
        """The method recommending random meals.

        Args:
            n (int, optional): The number of meals to recommend. Defaults to 3.

        Returns:
            List[dict]: A list of recommended meals as dictionaries.
        """


    @abstractmethod
    async def get_by_area(self, meal_area: str) -> Iterable[Any]:
        """The abstract method for getting a meal recipe by provided meal area.

        Args:
            meal_area (str): The area of the meal.

        Returns:
            Iterable[Any]: The meal details available.
        """

    @abstractmethod
    async def add_meal(self, data: MealBroker) -> Optional[Any]:
        """The abstract method for adding a meal to the data storage.

        Args:
            data (MealBroker): The details of the new meal.

        Returns:
            Any | None: The newly added meal.
        """

    @abstractmethod
    async def delete_meal(self, meal_id: int) -> bool:
        """The abstract method for deleting a meal from the data storage.

        Args:
            meal_id (int): The id of the meal.

        Returns:
            bool: True if the meal was successfully deleted.
        """

    @abstractmethod
    async def update_meal(self, meal_id: int, data: MealBroker) -> Optional[Any]:
        """The abstract method for updating a meal in the data storage.

        Args:
            meal_id (int): The id of the meal.
            data (MealBroker): The details of the new meal.

        Returns:
            Any | None: The newly updated meal.
        """

    @abstractmethod
    async def get_by_ingredients(self, ingredient_name: str) -> List[dict]:
        """The method getting meals by a specific ingredient.

        Args:
            ingredient_name (str): The name of the ingredient.

        Returns:
            List[dict]: Meals containing the specified ingredient.
        """