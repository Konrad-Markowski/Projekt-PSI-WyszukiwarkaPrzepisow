"""A module containing user-related routers."""

from typing import List
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException

from src.container import Container
from src.core.domain.user import UserIn
from src.infrastructure.dto.tokendto import TokenDTO
from src.infrastructure.dto.userdto import UserDTO
from src.infrastructure.services.iuser import IUserService
from pydantic import UUID4

router = APIRouter()


@router.post("/register", response_model=UserDTO, status_code=201)
@inject
async def register_user(
    user: UserIn,
    service: IUserService = Depends(Provide[Container.user_service]),
) -> dict:
    """A router coroutine for registering new user

    Args:
        user (UserIn): The user input data.
        service (IUserService, optional): The injected user service.

    Returns:
        dict: The user DTO details.
    """

    if new_user := await service.register_user(user):
        return UserDTO(**dict(new_user)).model_dump()

    raise HTTPException(
        status_code=400,
        detail="The user with provided e-mail already exists",
    )


@router.post("/token", response_model=TokenDTO, status_code=200)
@inject
async def authenticate_user(
    user: UserIn,
    service: IUserService = Depends(Provide[Container.user_service]),
) -> dict:
    """A router coroutine for authenticating users.

    Args:
        user (UserIn): The user input data.
        service (IUserService, optional): The injected user service.

    Returns:
        dict: The token DTO details.
    """

    if token_details := await service.authenticate_user(user):
        print("user confirmed")
        return token_details.model_dump()

    raise HTTPException(
        status_code=401,
        detail="Provided incorrect credentials",
    )


@router.get("/user/{uuid}", response_model=UserDTO, status_code=200)
@inject
async def get_user_by_uuid(
    uuid: UUID4,
    service: IUserService = Depends(Provide[Container.user_service]),
) -> dict:
    """A router coroutine for getting user by UUID.

    Args:
        uuid (UUID4): The UUID of the user.
        service (IUserService, optional): The injected user service.

    Returns:
        dict: The user DTO details.
    """

    if user := await service.get_by_uuid(uuid):
        return user.model_dump()

    raise HTTPException(
        status_code=404,
        detail="User not found",
    )


@router.get("/user/email/{email}", status_code=200)
@inject
async def get_user_by_email(
    email: str,
    service: IUserService = Depends(Provide[Container.user_service]),
) -> dict:
    """Retrieve a user by email."""
    user = await service.get_by_email(email)
    if user:
        return UserDTO(**user).model_dump()

    raise HTTPException(
        status_code=404,
        detail="User not found",
    )

@router.post("/user/favourites/{uuid}/add", status_code=201)
@inject
async def add_to_favourites(
    uuid: UUID4,
    meal_id: int,
    service: IUserService = Depends(Provide[Container.user_service]),
) -> dict:
    """Add a meal to the user's favourites."""
    added = await service.add_to_favourites(uuid, meal_id)
    if added:
        return {"message": "Meal added to favourites"}
    raise HTTPException(
        status_code=404,
        detail="Meal not found or already in favourites",
    )

@router.delete("/user/favourites/{uuid}/remove", status_code=200)
@inject
async def remove_from_favourites(
    uuid: UUID4,
    meal_id: int,
    service: IUserService = Depends(Provide[Container.user_service]),
) -> dict:
    """Remove a meal from the user's favourites.

    Args:
        uuid (UUID4): The UUID of the user.
        meal_id (int): The ID of the meal to be removed.
        service (IUserService, optional): The injected user service.

    Returns:
        dict: A message indicating the result of the operation.

    Raises:
        HTTPException: If the meal is not found in the user's favourites.
    """
    is_removed = await service.remove_from_favourites(uuid, meal_id)
    if is_removed:
        return {"message": "Meal removed from favourites"}
    raise HTTPException(
        status_code=404,
        detail="Meal not found in favourites",
    )


@router.get("/user/favourites/{uuid}", response_model=List[str])
@inject
async def get_favourites(
    uuid: UUID4,
    service: IUserService = Depends(Provide[Container.user_service]),
) -> list:
    """Get a list of the user's favourite meals."""
    favourites = await service.get_favourites(uuid)
    if favourites is not None:
        return favourites
    raise HTTPException(
        status_code=404,
        detail="User not found",
    )