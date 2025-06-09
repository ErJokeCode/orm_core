import logging
from typing import Any, Literal, Optional, Sequence, TypeVar, Generic, Union, overload
from uuid import UUID
from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import Result, Select, asc, delete, desc, func, inspect, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from .get_by import BasicModelGetByOperations


_log = logging.getLogger(__name__)


M = TypeVar('M')


class BasicModelEditOperations(BasicModelGetByOperations[M], Generic[M]):

    model: type[M]

    @overload
    async def edit(
        self,
        *,
        session: AsyncSession,
        id: UUID,
        edit_item: Union[dict]
    ) -> Union[M, None]: ...

    @overload
    async def edit(
        self,
        *,
        session: AsyncSession,
        id: UUID,
        edit_item: Union[dict],
        get_return: Literal[False]
    ) -> None: ...

    @overload
    async def edit(
        self,
        *,
        session: AsyncSession,
        id: UUID,
        edit_item: Union[dict],
        return_query: Select
    ) -> Optional[M]: ...

    @overload
    async def edit(
        self,
        *,
        session: AsyncSession,
        id: UUID,
        edit_item: Union[dict],
        return_query: Select,
        is_get_none: Literal[False]
    ) -> M: ...

    async def edit(
        self,

        *,

        session: AsyncSession,

        id: UUID,

        edit_item: Union[dict],

        get_return: bool = True,

        return_query: Union[Select, None] = None,

        is_get_none: bool = True

    ) -> Optional[M]:

        _log.info("Edit model %s", self.model.__name__)

        model = await session.get(self.model, id)

        if model is None:
            raise HTTPException(
                status_code=404, detail=f"{self.model.__name__} not found")

        if isinstance(edit_item, dict):
            for key, value in edit_item.items():
                if value is not None:
                    setattr(model, key, value)

        await session.flush()

        if get_return:

            if return_query is not None:

                if is_get_none:
                    return await super().get_by_query(
                        session=session,
                        query=return_query,
                        id=id,
                        is_get_none=True
                    )
                else:
                    return await super().get_by_query(
                        session=session,
                        query=return_query,
                        id=id
                    )

            return model

        return None
