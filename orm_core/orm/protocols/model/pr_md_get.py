from typing import (
    Generic, Optional, TypeVar, Protocol, Union, overload, Literal, Any
)
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select

M = TypeVar('M', covariant=True)


class ModelGetProtocol(Protocol[M]):
    @overload
    async def get_by_query(
        self,
        session: AsyncSession,
        query: Select,
        id: UUID,
        is_get_none: Literal[False] = False,
    ) -> M: ...

    @overload
    async def get_by_query(
        self,
        session: AsyncSession,
        query: Select,
        id: UUID,
        is_get_none: Literal[True] = True,
    ) -> Union[M, None]: ...

    async def get_by_query(
        self,
        session: AsyncSession,
        query: Select,
        id: Union[UUID, None] = None,
        is_get_none: bool = False,
    ) -> Union[M, None]:
        raise NotImplementedError
