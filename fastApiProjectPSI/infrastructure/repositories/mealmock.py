"""Module containing meal repository implementation."""

from typing import Iterable, Optional
from pydantic import BaseModel


meals = []

class Meal(BaseModel):
    """Model for the meal data."""
    idMeal: str
    strMeal: str
    strCategory: Optional[str]
    strArea: Optional[str]
    strInstructions: Optional[str]
    strMealThumb: Optional[str]
    strTags: Optional[str]
    strYoutube: Optional[str]
    ingredients: list[str] = []
    measures: list[str] = []


class MealIn(BaseModel):
    """Model for input meal data."""
    strMeal: str
    strCategory: Optional[str]
    strArea: Optional[str]
    strInstructions: Optional[str]
    strMealThumb: Optional[str]
    strTags: Optional[str]
    strYoutube: Optional[str]
    ingredients: list[str] = []
    measures: list[str] = []


class MealMockRepository:
    """A class representing a mock meal repository."""

    async def get_all_meals(self) -> Iterable[Meal]:
        """The method getting all meals from the data storage.

        Returns:
            Meals in the data storage.
        """
        return meals

    async def get_by_id(self, meal_id: str) -> Optional[Meal]:
        """The method getting a meal by its ID.

        Args:
            meal_id (str): The ID of the meal.

        Returns:
            The meal details, or None if not found.
        """
        return next((meal for meal in meals if meal.idMeal == meal_id), None)

    async def get_by_category(self, category: str) -> Iterable[Meal]:
        """The method getting meals by category.

        Args:
            category (str): The category of the meals.

        Returns:
            The filtered list of meals by category.
        """
        return [meal for meal in meals if meal.strCategory == category]

    async def get_by_area(self, area: str) -> Iterable[Meal]:
        """The method getting meals by area of origin.

        Args:
            area (str): The area of origin.

        Returns:
            The filtered list of meals by area.
        """
        return [meal for meal in meals if meal.strArea == area]

    async def add_meal(self, data: MealIn) -> Meal:
        """The method adding a new meal for the data storage.

        Args:
            data (MealIn): The details of the new meal.

        Returns:
            The newly added meal details.
        """
        new_meal = Meal(idMeal=str(len(meals) + 1), **data.dict())
        meals.append(new_meal)
        return new_meal

    async def update_meal(self, meal_id: str, data: MealIn) -> Optional[Meal]:
        """The method updating meal data in the data storage.

        Args:
            meal_id (str): The ID of the meal.
            data (MealIn): The updated meal details.

        Returns:
            The updated meal details, or None if not found.
        """
        for index, meal in enumerate(meals):
            if meal.idMeal == meal_id:
                updated_meal = Meal(idMeal=meal_id, **data.dict())
                meals[index] = updated_meal
                return updated_meal
        return None

    async def delete_meal(self, meal_id: str) -> bool:
        """The method that removes a meal from the data storage.

        Args:
            meal_id (str): The ID of the meal.

        Returns:
            bool: Success of the operation.
        """
        global meals
        initial_count = len(meals)
        meals = [meal for meal in meals if meal.idMeal != meal_id]
        return len(meals) < initial_count
