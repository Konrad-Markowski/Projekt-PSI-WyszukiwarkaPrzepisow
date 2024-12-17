from typing import Optional, List
from pydantic import BaseModel, ConfigDict

from asyncpg import Record  # type: ignore

class MealDTO(BaseModel):
    """A model representing DTO for meal data."""
    strMeal: str
    strCategory: Optional[str]
    strArea: Optional[str]
    strInstructions: str
    strMealThumb: Optional[str]
    strTags: Optional[str]
    strYoutube: Optional[str]
    ingredients: List[str] = []
    measures: List[str] = []

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )

    @classmethod
    def from_record(rec, record: Record) -> "MealDTO":
        """A method for preparing DTO instance based on DB record.

        Args:
            record (Record): The DB record.

        Returns:
            MealDTO: The final DTO instance.
        """
        record_dict = dict(record)

        return rec(
            strMeal=record_dict.get("strMeal"),  # type: ignore
            strCategory=record_dict.get("strCategory"),  # type: ignore
            strArea=record_dict.get("strArea"),  # type: ignore
            strInstructions=record_dict.get("strInstructions"),  # type: ignore
            strMealThumb=record_dict.get("strMealThumb"),  # type: ignore
            strTags=record_dict.get("strTags"),  # type: ignore
            strYoutube=record_dict.get("strYoutube"),  # type: ignore
            ingredients=record_dict.get("ingredients", []),  # type: ignore
            measures=record_dict.get("measures", []),  # type: ignore
        )
    