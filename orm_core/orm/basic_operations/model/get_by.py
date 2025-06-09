import logging
from typing import Any, Literal, Optional, Sequence, TypeVar, Generic, Union, overload
from uuid import UUID
from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import Result, Select, asc, delete, desc, func, inspect, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload


_log = logging.getLogger(__name__)


M = TypeVar('M')


class BasicModelGetByOperations(Generic[M]):

    model: type[M]

    @overload
    async def get_by(
        self,
        session: AsyncSession,
        id: UUID,
        loads: dict[str, str],
        is_get_none: Literal[True],
        **kwargs
    ) -> Optional[M]: ...

    @overload
    async def get_by(
        self,
        session: AsyncSession,
        id: UUID,
        loads: dict[str, str],
        **kwargs
    ) -> M: ...

    @overload
    async def get_by(
        self,
        session: AsyncSession,
        id: UUID,
        **kwargs
    ) -> M: ...

    async def get_by(
        self,
        session: AsyncSession,
        id: Optional[UUID] = None,
        loads: Optional[dict[str, str]] = None,
        is_get_none: bool = False,
        **kwargs
    ) -> Optional[M]:
        _log.info("Get by kwargs %s", self.model.__name__)

        query = select(
            self.model
        )

        if id is not None:
            query = query.filter_by(id=id)

        query = query.filter_by(
            **kwargs
        )

        if loads is not None:
            for key, value in loads.items():
                if key == "s":
                    query = query.options(
                        selectinload(getattr(self.model, value))
                    )
                elif key == "j":
                    query = query.options(
                        joinedload(getattr(self.model, value))
                    )

        result = await session.execute(query)
        item = result.scalars().first()

        if item is None:
            if is_get_none:
                return None
            raise HTTPException(
                status_code=404, detail=f"{self.model.__name__} not found")

        return item

    @overload
    async def get_by_query(
        self,
        *,
        session: AsyncSession,
        query: Select,
        id: UUID,
    ) -> M: ...

    @overload
    async def get_by_query(
        self,
        *,
        session: AsyncSession,
        query: Select,
    ) -> M: ...

    @overload
    async def get_by_query(
        self,
        *,
        session: AsyncSession,
        query: Select,
        id: UUID,
        is_get_none: Literal[True],
    ) -> Optional[M]: ...

    @overload
    async def get_by_query(
        self,
        *,
        session: AsyncSession,
        query: Select,
        is_get_none: Literal[True],
    ) -> Optional[M]: ...

    async def get_by_query(
        self,

        *,

        session: AsyncSession,

        query: Select,

        id: Union[UUID, None] = None,

        is_get_none: bool = False,

    ) -> Optional[M]:

        _log.info("Get model by query %s", self.model.__name__)

        if id is not None:
            query = query.filter_by(id=id)

        result = await session.execute(query)
        model = result.scalars().first()

        if model is None:
            if is_get_none:
                return None
            raise HTTPException(
                status_code=404, detail=f"{self.model.__name__} not found")

        return model
