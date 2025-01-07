from typing import Optional, List

from pydantic import BaseModel, UUID4, ConfigDict


class MealIn(BaseModel):
    """Model representing airport's DTO attributes."""
    strMeal: str
    strInstructions: str
    ingredients: List[str] = []
    measures: List[str] = []
    strCategory: Optional[str] = None
    strArea: Optional[str] = None
    strMealThumb: Optional[str] = None
    strTags: Optional[str] = None
    strYoutube: Optional[str] = None



class MealBroker(MealIn):
    """A broker class introducing user in the model"""
    user_id: UUID4


class Meal(MealBroker):
    """Model representing meal's attributes in the database"""
    id: int


    model_config = ConfigDict(from_attributes=True, extra="ignore")