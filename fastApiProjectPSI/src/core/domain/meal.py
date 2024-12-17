from typing import Optional

from pydantic import BaseModel, UUID4, ConfigDict


class MealIn(BaseModel):
    """Model for input meal data."""
    strMeal: str
    strCategory: Optional[str]
    strArea: Optional[str]
    strInstructions: str
    strMealThumb: Optional[str]
    strTags: Optional[str]
    strYoutube: Optional[str]
    ingredients: list[str] = []
    measures: list[str] = []



class MealBroker(MealIn):
    """A broker class introducing user in the model"""
    user_id: UUID4


class Meal(MealBroker):
    """Model representing meal's attributes in the database"""
    id: int


    model_config = ConfigDict(from_attributes=True, extra="ignore")