from functools import wraps
from typing import Callable

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from database import models
from utils.config import DATABASE_URL


engine = create_async_engine(
    url=DATABASE_URL,
    pool_pre_ping=True,
)
async_session = async_sessionmaker(bind=engine, expire_on_commit=False)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(models.get_base_model().metadata.create_all)


def db_session(func: Callable):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        async with async_session() as session:
            return await func(*args, session=session, **kwargs)
    return wrapper


def class_db_session(func: Callable):
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        async with async_session() as session:
            self.session = session
            return await func(self, *args, **kwargs)
    return wrapper
