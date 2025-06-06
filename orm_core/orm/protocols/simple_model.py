from typing import (
    Generic, Optional, TypeVar, Protocol, overload, Literal, Any
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select

M = TypeVar('M')


class SimpleModelOrmProtocol(Protocol[M]):
    @overload
    async def add(
        self,
        session: AsyncSession,
        data: M
    ) -> M: ...

    @overload
    async def add(
        self,
        session: AsyncSession,
        data: M,
        return_query: Select
    ) -> M: ...

    async def add(
        self,
        session: AsyncSession,
        data: M,
        return_query: Optional[Select] = None,
    ) -> M:
        raise NotImplementedError
