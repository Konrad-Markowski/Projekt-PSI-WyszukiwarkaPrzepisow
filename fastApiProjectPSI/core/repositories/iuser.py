from abc import ABC, abstractmethod
from typing import Any

from pydantic import UUID5, EmailStr

from core.domain.user import UserIn


class IUserRepository(ABC):


    @abstractmethod
    async def register_user(self, user: UserIn) -> Any | None:
        """A method to register a user"""



    @abstractmethod
    async def get_by_uuid(self, uuid: UUID5) -> Any | None:
        """A method to retrieve a user by his UUID"""


    @abstractmethod
    async def get_by_email(self, email: EmailStr) -> Any | None:
        """A method to retrieve a user by his email"""