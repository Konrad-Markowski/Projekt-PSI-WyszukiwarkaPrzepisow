"""Module containing meal service abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable

from src.core.domain.meal import Meal, MealBroker
from src.infrastructure.dto.mealdto import MealDTO


class IMealService(ABC):
    """A class representing meal repository"""

    @abstractmethod
    async def get_all_meals(self) -> Iterable[MealDTO]:
        """
        The abstract method for getting all meals from the database.

        Args:
            None.

        Returns:
            Iterable[Any]
        """

    @abstractmethod
    async def get_by_id(self, meal_id: int) -> Iterable[MealDTO] | None:
        """The abstract method for getting a meal recipe by provided id.

        Args:
            meal_id (int): The id of the meal.

        Returns:
            Any | None: The meal details available.
        """

    @abstractmethod
    async def get_by_name(self, meal_name: str) -> Iterable[MealDTO]:
        """The abstract method for getting a meal recipe by provided meal name.

        Args:
            meal_name (str): The name of the meal.

        Returns:
            Any | None: The meal details available.
        """

    @abstractmethod
    async def get_by_category(self, meal_category: str) -> Iterable[MealDTO]:
        """The abstract method for getting a meal recipe by provided meal category.

        Args:
            meal_category (str): The category of the meal.

        Returns:
            Any | None: The meal details available.
        """

    @abstractmethod
    async def get_by_area(self, meal_area: str) -> Iterable[MealDTO]:
        """The abstract method for getting a meal recipe by provided meal area.

        Args:
            meal_area (str): The area of the meal.

        Returns:
            Any | None: The meal details available.
        """

    @abstractmethod
    async def add_meal(self, data: MealBroker) -> Meal | None:
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
    async def update_meal(self, meal_id: int, data: MealBroker) -> Meal | None:
        """The abstract method for updating a meal in the data storage.

        Args:
            meal_id (int): The id of the meal.
            data (MealBroker): The details of the new meal.

        Returns:
            Any | None: The newly updated meal.
        """