import logging
from typing import Any, Literal, Optional, Sequence, TypeVar, Generic, Union, overload
from uuid import UUID
from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import Result, Select, asc, delete, desc, func, inspect, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from orm_core.base_schemes import ListDTO, ResponseStatus
from orm_core.base import Base


_log = logging.getLogger(__name__)


M = TypeVar('M')
A = TypeVar('A', bound=BaseModel, default=Any)
E = TypeVar('E', bound=BaseModel, default=Any)
O = TypeVar('O', bound=BaseModel, default=Any)


class BasicGetOperations(Generic[M, A, E, O]):

    model: type[M]
    input_scheme: type[A]
    edit_scheme: type[E]
    out_scheme: type[O]

    async def get_by_query(
        self,
        session: AsyncSession,
        query: Select,
        id: Union[UUID, None] = None,
        is_model: bool = True,
        is_get_none: bool = True,
    ) -> Union[O, M, None]:
        _log.info("Get by query %s", self.model.__name__)

        if id is not None:
            query = query.filter_by(id=id)

        result = await session.execute(query)
        model = result.scalars().first()

        if model is None:
            if is_get_none:
                return None
            raise HTTPException(
                status_code=404, detail=f"{self.model.__name__} not found")

        if is_model:
            return model

        return self.out_scheme.model_validate(model)
