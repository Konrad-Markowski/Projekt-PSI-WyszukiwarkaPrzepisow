"""A module containing meal endpoints"""


from typing import Iterable

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt

from src.infrastructure.utils import consts
from src.container import Container
from src.core.domain.meal import Meal, MealIn, MealBroker
from src.infrastructure.dto.mealdto import MealDTO
from src.infrastructure.services.imeal import IMealService

bearer_scheme = HTTPBearer()

router = APIRouter()


@router.post("/create", response_model=Meal, status_code=201)
@inject
async def create_meal(
    meal: MealIn,
    service: IMealService = Depends(Provide[Container.meal_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """An endpoint for adding new meal.

    Args:
        meal (MealIn): The meal data.
        service (IMealService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Returns:
        dict: The new meal attributes.
    """

    token = credentials.credentials
    token_payload = jwt.decode(
        token,
        key=consts.SECRET_KEY,
        algorithms=[consts.ALGORITHM],
    )
    user_uuid = token_payload.get("sub")

    if not user_uuid:
        raise HTTPException(status_code=403, detail="Unauthorized")

    extended_meal_data = MealBroker(
        user_id=user_uuid,
        **meal.model_dump(),
    )
    new_meal = await service.add_meal(extended_meal_data)

    return new_meal.model_dump() if new_meal else {}


@router.get("/all", response_model=Iterable[MealDTO], status_code=200)
@inject
async def get_all_meals(
    service: IMealService = Depends(Provide[Container.meal_service]),
) -> Iterable:
    """An endpoint for getting all meals.

    Args:
        service (IMealService, optional): The injected service dependency.

    Returns:
        Iterable: The meal attributes collection.
    """

    meals = await service.get_all_meals()

    return meals


@router.get(
        "/{meal_id}",
        response_model=MealDTO,
        status_code=200,
)
@inject
async def get_meal_by_id(
    meal_id: int,
    service: IMealService = Depends(Provide[Container.meal_service]),
) -> dict | None:
    """An endpoint for getting meal by id.

    Args:
        meal_id (int): The id of the meal.
        service (IMealService, optional): The injected service dependency.

    Returns:
        dict | None: The meal details.
    """

    if meal := await service.get_by_id(meal_id):
        return meal.model_dump()

    raise HTTPException(status_code=404, detail="Meal not found")


@router.put("/{meal_id}", response_model=Meal, status_code=201)
@inject
async def update_meal(
    meal_id: int,
    updated_meal: MealIn,
    service: IMealService = Depends(Provide[Container.meal_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """An endpoint for updating meal data.

    Args:
        meal_id (int): The id of the meal.
        updated_meal (MealIn): The updated meal details.
        service (IMealService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException: 404 if meal does not exist.

    Returns:
        dict: The updated meal details.
    """

    token = credentials.credentials
    token_payload = jwt.decode(
        token,
        key=consts.SECRET_KEY,
        algorithms=[consts.ALGORITHM],
    )
    user_uuid = token_payload.get("sub")

    if not user_uuid:
        raise HTTPException(status_code=403, detail="Unauthorized")

    if meal_data := await service.get_by_id(meal_id=meal_id):
        if str(meal_data.user_id) != user_uuid:
            raise HTTPException(status_code=403, detail="Unauthorized")

        extended_updated_meal = MealBroker(
            user_id=user_uuid,
            **updated_meal.model_dump(),
        )
        updated_meal_data = await service.update_meal(
            meal_id=meal_id,
            data=extended_updated_meal,
        )
        return updated_meal_data.model_dump() if updated_meal_data \
            else {}

    raise HTTPException(status_code=404, detail="Meal not found")


@router.delete("/{meal_id}", status_code=204)
@inject
async def delete_meal(
    meal_id: int,
    service: IMealService = Depends(Provide[Container.meal_service]),
) -> None:
    """An endpoint for deleting meals.

    Args:
        meal_id (int): The id of the meal.
        service (IMealService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if meal does not exist.
    """

    if await service.get_by_id(meal_id=meal_id):
        await service.delete_meal(meal_id)

        return

    raise HTTPException(status_code=404, detail="Meal not found")
