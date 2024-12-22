from datetime import datetime, UTC
from typing import TypeVar, Generic, Type, List, Union, Optional

from sqlalchemy import select, update, and_, ClauseElement

from database.database import async_session
from database.models.base import BaseModel


class ModelDoesNotExist(Exception):
    pass


ModelType = TypeVar('ModelType', bound=BaseModel)


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def create(self, **kwargs) -> ModelType:
        obj = self.model(**kwargs)

        async with async_session() as session:
            session.add(obj)
            await session.commit()
            await session.refresh(obj)

        return obj

    async def get(
            self,
            *filters: Union[ClauseElement, List[ClauseElement]],
            include_deleted=False,
    ) -> ModelType:
        query = await self._create_select_query(*filters, include_deleted=include_deleted)

        async with async_session() as session:
            async with session.begin():
                raw_result = await session.execute(query)
        result = raw_result.scalar_one_or_none()

        if not result:
            raise ModelDoesNotExist()

        return result

    async def get_or_none(
            self,
            *filters: Union[ClauseElement, List[ClauseElement]],
            include_deleted=False,
    ) -> Optional[ModelType]:
        try:
            result = await self.get(*filters, include_deleted=include_deleted)
        except ModelDoesNotExist:
            result = None
        return result

    async def get_all(
            self,
            *filters: Union[ClauseElement, List[ClauseElement]],
            include_deleted=False,
    ) -> List[ModelType]:
        query = await self._create_select_query(*filters, include_deleted=include_deleted)

        async with async_session() as session:
            raw_result = await session.execute(query)

        return raw_result.scalars().all()

    async def get_by_index(
            self,
            index: int = 0,
            *filters: Union[ClauseElement, List[ClauseElement]],
            include_deleted=False,
    ) -> ModelType:
        raw_result = await self.get_all(*filters, include_deleted=include_deleted)
        if not raw_result:
            raise ModelDoesNotExist()
        return raw_result[index]

    async def get_first(self, *filters: Union[ClauseElement, List[ClauseElement]], include_deleted=False) -> ModelType:
        return await self.get_by_index(index=0, include_deleted=include_deleted, *filters)

    async def get_last(self, *filters: Union[ClauseElement, List[ClauseElement]], include_deleted=False) -> ModelType:
        return await self.get_by_index(index=-1, include_deleted=include_deleted, *filters)

    async def update(self, id_: int, include_deleted=False, **kwargs) -> ModelType:
        query = await self._create_update_query(id_=id_, updated_at=datetime.now(UTC), **kwargs)

        async with async_session() as session:
            async with session.begin():
                await session.execute(query)
                await session.commit()
        return await self.get_by_id(id_, include_deleted=include_deleted)

    async def delete(self, id_: int) -> ModelType:
        return await self.update(id_=id_, is_deleted=True, include_deleted=True)

    async def get_by_id(self, id_: int, include_deleted: bool = False) -> ModelType:
        return await self.get(and_(self.model.id == id_), include_deleted=include_deleted)

    async def _create_select_query(
            self,
            *filters: Union[ClauseElement, List[ClauseElement]],
            include_deleted: bool = False,
            synchronize_session: str = None,
    ):
        query = select(self.model)
        if filters:
            query = query.where(and_(*filters))
        if not include_deleted:
            query = query.where(and_(self.model.is_deleted == False))
        if synchronize_session:
            query = query.execution_options(
                synchronize_session=synchronize_session,
            )

        return query

    async def _create_update_query(
            self,
            id_: int,
            **kwargs
    ):
        query = (
            update(self.model)
            .where(and_(self.model.id == id_))
            .values(**kwargs)
            .execution_options(synchronize_session='fetch')
        )
        return query
