from typing import Optional, List
from pydantic import BaseModel, ConfigDict, UUID4

from asyncpg import Record  # type: ignore

class MealDTO(BaseModel):
    """A model representing DTO for meal data."""
    id: int
    strMeal: str
    strInstructions: str
    ingredients: List[str] = []
    measures: List[str] = []
    strCategory: Optional[str] = None
    strArea: Optional[str] = None
    strMealThumb: Optional[str] = None
    strTags: Optional[str] = None
    strYoutube: Optional[str] = None
    user_id: UUID4

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )

    @classmethod
    def from_record(cls, record: Record) -> "MealDTO":
        """A method for preparing DTO instance based on DB record.

        Args:
            record (Record): The DB record.

        Returns:
            MealDTO: The final DTO instance.
        """
        record_dict = dict(record)

        return cls(
            id=record_dict.get("id"),  # type: ignore
            strMeal=record_dict.get("strMeal"),  # type: ignore
            strInstructions=record_dict.get("strInstructions"),  # type: ignore
            ingredients=record_dict.get("ingredients", []),  # type: ignore
            measures=record_dict.get("measures", []),  # type: ignore
            strCategory=record_dict.get("strCategory"),  # type: ignore
            strArea=record_dict.get("strArea"),  # type: ignore
            strMealThumb=record_dict.get("strMealThumb"),  # type: ignore
            strTags=record_dict.get("strTags"),  # type: ignore
            strYoutube=record_dict.get("strYoutube"),  # type: ignore
            user_id=record_dict.get("user_id"),  # type: ignore
        )