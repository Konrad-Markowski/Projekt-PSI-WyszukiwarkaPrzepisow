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


#make services and container.py