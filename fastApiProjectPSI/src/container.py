from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory, Singleton
from src.infrastructure.repositories.user import UserRepository
from src.infrastructure.repositories.mealdb import MealRepository
from src.infrastructure.services.user import UserService
from src.infrastructure.services.meal import MealService

"""Module providing containers injecting dependencies."""




class Container(DeclarativeContainer):
    """Container class for dependency injecting purposes."""
    user_repository = Singleton(UserRepository)
    meal_repository = Singleton(MealRepository)
    #recommended_meal_repository = Singleton(RecommendedMealRepository)
    #favourite_meal_repository = Singleton(FavouriteMealRepository)

    user_service = Factory(
        UserService,
        repository=user_repository,
    )
    meal_service = Factory(
        MealService,
        repository=meal_repository,
    )