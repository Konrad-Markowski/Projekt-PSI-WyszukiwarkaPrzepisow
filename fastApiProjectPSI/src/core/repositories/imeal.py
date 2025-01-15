"""Module containing meal repository abstractions"""

from abc import ABC, abstractmethod
from typing import Any, Iterable, List

from src.infrastructure.dto.mealdto import MealDTO
from src.core.domain.meal import MealBroker

class IMealRepository(ABC):
    """An abstract class representing a meal repository"""

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
    async def get_by_id(self, meal_id: int) -> Any | None:
        """The abstract method for getting a meal recipe by provided id.

        Args:
            meal_id (int): The id of the meal.

        Returns:
            Any | None: The meal details available.
        """

    @abstractmethod
    async def get_by_user(self, user_id: int) -> Iterable[Any]:
        """The abstract getting meals by user who added them.

        Args:
            user_id (int): The id of the user.

        Returns:
            Iterable[Any]: The meal collection.
        """

    @abstractmethod
    async def get_by_name(self, meal_name: str) -> Any | None:
        """The abstract method for getting a meal recipe by provided meal name.

        Args:
            meal_name (str): The name of the meal.

        Returns:
            Any | None: The meal details available.
        """

    @abstractmethod
    async def get_by_category(self, meal_category: str) -> Any | None:
        """The abstract method for getting a meal recipe by provided meal category.

        Args:
            meal_category (str): The category of the meal.

        Returns:
            Any | None: The meal details available.
        """

    @abstractmethod
    async def get_by_area(self, meal_area: str) -> Any | None:
        """The abstract method for getting a meal recipe by provided meal area.

        Args:
            meal_area (str): The area of the meal.

        Returns:
            Any | None: The meal details available.
        """

    @abstractmethod
    async def add_meal(self, data: MealBroker) -> Any | None:
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
    async def update_meal(self, meal_id: int, data: MealBroker) -> Any | None:
        """The abstract method for updating a meal in the data storage.

        Args:
            meal_id (int): The id of the meal.
            data (MealBroker): The details of the new meal.

        Returns:
            Any | None: The newly updated meal.
        """

    @abstractmethod
    async def recommend_meals(self, n: int = 3) -> List[MealDTO]:
        """The method recommending random meals.

        Args:
            n (int, optional): The number of meals to recommend. Defaults to 3.

        Returns:
            List[MealDTO]: A list of recommended meals.
        """