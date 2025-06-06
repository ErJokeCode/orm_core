import logging
from typing import Any, Literal, Optional, Sequence, TypeVar, Generic, Union, overload
from uuid import UUID
from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import Result, Select, asc, delete, desc, func, inspect, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from orm_core.orm.basic_operations.basic_operation_get import BasicGetOperations


_log = logging.getLogger(__name__)


M = TypeVar('M')
I = TypeVar('I', bound=BaseModel)
E = TypeVar('E', bound=BaseModel)
O = TypeVar('O', bound=BaseModel)


class BasicEditOperations(BasicGetOperations, Generic[M, I, E, O]):

    model: type[M]
    input_scheme: type[I]
    edit_schema: type[E]
    out_scheme: type[O]

    async def edit(
        self,
        session: AsyncSession,
        id: Union[UUID, int],
        edit_item: Union[E, dict],
        is_model: bool = True,
        return_query: Union[Select, None] = None
    ) -> Union[O, M, None]:
        _log.info("Edit %s", self.model.__name__)

        model = await session.get(self.model, id)

        if model is None:
            raise HTTPException(
                status_code=404, detail=f"{self.model.__name__} not found")

        if isinstance(edit_item, dict):
            for key, value in edit_item.items():
                if value is not None:
                    setattr(model, key, value)
        else:
            for key, value in edit_item.model_dump().items():
                if value is not None:
                    setattr(model, key, value)

        await session.flush()

        if return_query is not None:
            if is_model:
                return await self.get_by_query(
                    session=session,
                    query=return_query,
                    is_model=True,
                    is_get_none=False
                )

            return await self.get_by_query(
                session=session,
                query=return_query,
                is_model=False,
                is_get_none=False
            )

        if is_model:
            return model

        return self.out_scheme.model_validate(model)
