from typing import Iterable

from fastapi import FastAPI, HTTPException, Body
from infrastructure.repositories.mealmock import MealMockRepository, Meal, MealIn

app = FastAPI()
meal_repository = MealMockRepository()


@app.get("/")
async def root() -> dict:
    return {"message": "Meal API project made for PSI classes"}


@app.get("/recipe/{recipeName}")
async def find_recipe_by_name(recipeName: str):
    """Fetch recipe details by name from the mock database.

    Args:
        recipeName (str): Name of the recipe to search.

    Returns:
        Recipe details.
    """
    recipes = await meal_repository.get_all_meals()
    matching_recipes = [
        meal for meal in recipes if recipeName.lower() in meal.strMeal.lower()
    ]

    if not matching_recipes:
        raise HTTPException(status_code=404, detail="Recipe not found")

    return {"recipes": matching_recipes}


@app.get("/meals")
async def get_all_meals() -> Iterable[Meal]:
    """Fetch all meals from the mock database."""
    return await meal_repository.get_all_meals()


@app.get("/meals/{meal_id}")
async def get_meal_by_id(meal_id: str):
    """Fetch a single meal by ID from the database."""
    meal = await meal_repository.get_by_id(meal_id)
    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found")
    return meal


@app.get("/meals/category/{category}")
async def get_meals_by_category(category: str):
    """Fetch meals by category.

    Args:
        The category of the meals to fetch.

    Returns:
        The filtered list of meals by category.
    """
    meals = await meal_repository.get_by_category(category)
    if not meals:
        raise HTTPException(status_code=404, detail="No meals found for the specified category.")
    return {"category": category, "meals": meals}


@app.get("/meals/area/{area}")
async def get_meals_by_area(area: str):
    """Fetch meals by area of origin.

    Args:
        area (str): The area of origin to search.

    Returns:
        The filtered list of meals by area.
    """
    meals = await meal_repository.get_by_area(area)
    if not meals:
        raise HTTPException(status_code=404, detail="No meals found for the specified area.")
    return {"area": area, "meals": meals}


@app.post("/meals")
async def add_meal(meal: MealIn):
    """Add a new meal to the database."""
    new_meal = await meal_repository.add_meal(meal)
    return new_meal


@app.put("/meals/{meal_id}")
async def update_meal(
    meal_id: str,
    meal: MealIn = Body(
        ...,
        example={
            "strMeal": "String",
            "strCategory": "String",
            "strArea": "String",
            "strInstructions": "String",
            "strMealThumb": "https://example.com/image.jpg",
            "strTags": "String",
            "strYoutube": "https://youtube.com/example",
            "ingredients": ["string"],
            "measures": ["string"],
        },
    ),
):
    """Update an existing meal in the database."""
    existing_meal = await meal_repository.get_by_id(meal_id)
    if not existing_meal:
        raise HTTPException(status_code=404, detail="Meal not found")

    updated_meal = await meal_repository.update_meal(meal_id, meal)
    if not updated_meal:
        raise HTTPException(status_code=404, detail="Meal not found")
    return updated_meal


@app.delete("/meals/{meal_id}")
async def delete_meal(meal_id: str):
    """Delete a meal from the database."""
    success = await meal_repository.delete_meal(meal_id)
    if not success:
        raise HTTPException(status_code=404, detail="Meal not found")
    return {"message": f"Meal with ID {meal_id} deleted successfully!"}
