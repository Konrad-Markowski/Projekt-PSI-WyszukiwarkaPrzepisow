"""A module providing database access."""

import asyncio

import databases
import sqlalchemy
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.exc import OperationalError, DatabaseError
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.mutable import MutableList
from src.config import config
from asyncpg.exceptions import (    # type: ignore
    CannotConnectNowError,
    ConnectionDoesNotExistError,
)

metadata = sqlalchemy.MetaData()

user_table = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column(
        "id",
        UUID(as_uuid=True),
        primary_key=True,
        server_default=sqlalchemy.text("gen_random_uuid()"),
    ),
    sqlalchemy.Column("email", sqlalchemy.String, unique=True),
    sqlalchemy.Column("password", sqlalchemy.String),
    sqlalchemy.Column(
        "favourites",
        sqlalchemy.ARRAY(sqlalchemy.String),
        nullable=True,
        default=[],
    ),
)

meal_table = sqlalchemy.Table(
    "meals",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("strMeal", sqlalchemy.String),
    sqlalchemy.Column("strInstructions", sqlalchemy.String),
    sqlalchemy.Column(
        "ingredients",
        sqlalchemy.ARRAY(sqlalchemy.String),
        nullable=True,
        default=[],
    ),
    sqlalchemy.Column(
        "measures",
        sqlalchemy.ARRAY(sqlalchemy.String),
        nullable=True,
        default=[],
    ),
    sqlalchemy.Column("strCategory", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("strArea", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("strMealThumb", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("strTags", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("strYoutube", sqlalchemy.String, nullable=True),
    sqlalchemy.Column(
        "user_id",
        UUID(as_uuid=True),
        sqlalchemy.ForeignKey("users.id"),
        nullable=False,
    ),
    sqlalchemy.ForeignKeyConstraint(['user_id'], ['users.id'])
)

db_uri = (
    f"postgresql+asyncpg://{config.DB_USER}:{config.DB_PASSWORD}"
    f"@{config.DB_HOST}/{config.DB_NAME}"
)

engine = create_async_engine(
    db_uri,
    echo=True,
    future=True,
    pool_pre_ping=True,
)

database = databases.Database(
    db_uri,
    # force_rollback=True,
)


async def init_db(retries: int = 5, delay: int = 10) -> None:
    """Function initializing the DB.

    Args:
        retries (int, optional): Number of retries of connect to DB.
            Defaults to 5.
        delay (int, optional): Delay of connect do DB. Defaults to 2.
    """

    await asyncio.sleep(delay)
    for attempt in range(retries):
        try:
            async with engine.begin() as conn:
                await conn.run_sync(metadata.create_all)
            return
        except (
            OperationalError,
            DatabaseError,
            CannotConnectNowError,
            ConnectionDoesNotExistError,
        ) as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            await asyncio.sleep(delay)

    raise ConnectionError("Could not connect to DB after several retries.")
