import logging
from typing import Any, Literal, Optional, Sequence, TypeVar, Generic, Union, overload
from uuid import UUID
from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import Result, Select, asc, delete, desc, func, inspect, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..bs_op_model.md_add import BasicModelAddOperations


_log = logging.getLogger(__name__)


M = TypeVar('M')
A = TypeVar('A', bound=BaseModel, default=Any)
E = TypeVar('E', bound=BaseModel, default=Any)
O = TypeVar('O', bound=BaseModel, default=Any)


class BasicAddSchemeOperations(Generic[M, A, E, O]):

    model: type[M]
    input_scheme: type[A]
    edit_scheme: type[E]
    out_scheme: type[O]

    model_operation: BasicModelAddOperations[M]

    @overload
    async def add(
        self,
        session: AsyncSession,
        *,
        data: Union[A, M, dict],
    ) -> M: ...

    @overload
    async def add(
        self,
        session: AsyncSession,
        *,
        data: Union[A, M, dict],
        return_query: Select
    ) -> M: ...

    @overload
    async def add(
        self,
        session: AsyncSession,
        *,
        data: Union[A, M, dict],
        is_model: Literal[False]
    ) -> O: ...

    @overload
    async def add(
        self,
        session: AsyncSession,
        *,
        data: Union[A, M, dict],
        is_model: Literal[False],
        return_query: Select
    ) -> O: ...

    @overload
    async def add(
        self,
        session: AsyncSession,
        data: A,
        is_return: Literal[False]
    ) -> None: ...

    @overload
    async def add(
        self,
        session: AsyncSession,
        data: Union[A, M, dict],
        is_return: bool = True,
        is_model: bool = True,
        return_query: Union[Select, None] = None
    ) -> Union[M, O, None]: ...

    async def add(
        self,
        session: AsyncSession,
        data: Union[A, M, dict],
        is_return: bool = True,
        is_model: bool = True,
        return_query: Union[Select, None] = None
    ) -> Union[M, O, None]:
        _log.info("Add %s", self.model.__name__)

        if isinstance(data, self.model):
            model = data
        elif isinstance(data, dict):
            model = self.model(**data)
        else:
            model = self.model(**data.model_dump())  # type: ignore

        return_model = await self.model_operation.add(
            session=session,
            data=model,
            is_return=is_return,
            return_query=return_query
        )

        if is_model:
            return return_model

        return self.out_scheme.model_validate(return_model)
