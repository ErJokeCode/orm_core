from typing import (
    Generic, Optional, TypeVar, Protocol, Union, overload, Literal, Any
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select

M = TypeVar('M')


class ModelAddProtocol(Protocol[M]):
    @overload
    async def add(
        self,
        session: AsyncSession,
        *,
        data: Union[M, dict]
    ) -> M:
        ...

    @overload
    async def add(
        self,
        session: AsyncSession,
        *,
        data: Union[M, dict],
        loads: dict[str, str]
    ) -> M:
        ...

    @overload
    async def add(
        self,
        session: AsyncSession,
        *,
        data: Union[M, dict],
        return_query: Select
    ) -> M:
        ...

    @overload
    async def add(
        self,
        session: AsyncSession,
        *,
        data: Union[M, dict],
        is_return: Literal[False] = False
    ) -> None:
        ...

    @overload
    async def add(
        self,
        session: AsyncSession,
        data: Union[M, dict],
        is_return: bool = True,
        loads: Optional[dict[str, str]] = None,
        return_query: Optional[Select] = None
    ) -> Optional[M]:
        ...

    async def add(
        self,

        session: AsyncSession,

        data: Union[M, dict],

        is_return: bool = True,

        loads: Optional[dict[str, str]] = None,

        return_query: Optional[Select] = None

    ) -> Optional[M]:

        raise NotImplementedError
