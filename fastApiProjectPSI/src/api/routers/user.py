"""A module containing user-related routers."""

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


@router.get("/user/email/{email}", response_model=UserDTO, status_code=200)
@inject
async def get_user_by_email(
    email: str,
    service: IUserService = Depends(Provide[Container.user_service]),
) -> dict:
    """A router coroutine for getting user by email.

    Args:
        email (str): The email of the user.
        service (IUserService, optional): The injected user service.

    Returns:
        dict: The user DTO details.
    """

    if user := await service.get_by_email(email):
        return user.model_dump()

    raise HTTPException(
        status_code=404,
        detail="User not found",
    )

@router.post("/user/{uuid}/recommendations", status_code=200)
@inject
async def get_recommendations(
    uuid: UUID4,
    service: IUserService = Depends(Provide[Container.user_service]),
) -> dict:
    """Endpoint to get meal recommendations for a user.

    Args:
        uuid (UUID4): The UUID of the user.
        service (IUserService, optional): The injected user service.

    Returns:
        dict: The recommended meals.
    """

    recommendations = await service.recommend_meals(uuid)
    return {"recommendations": recommendations}

# modify later
'''@router.post("/user/{uuid}/favorites/{meal_id}", status_code=200)
@inject
async def add_meal_to_favorites(
    uuid: UUID4,
    meal_id: str,
    service: IUserService = Depends(Provide[Container.user_service]),
) -> dict:
    """A router coroutine for adding a meal to user's favorites.

    Args:
        uuid (UUID4): The UUID of the user.
        meal_id (str): The ID of the meal to add to favorites.
        service (IUserService, optional): The injected user service.

    Returns:
        dict: The updated user DTO details.
    """

    if updated_user := await service.add_meal_to_favorites(uuid, meal_id):
        return updated_user.model_dump()

    raise HTTPException(
        status_code=400,
        detail="Failed to add meal to favorites",
    )
'''