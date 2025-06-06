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
I = TypeVar('I', bound=BaseModel)
E = TypeVar('E', bound=BaseModel)
O = TypeVar('O', bound=BaseModel)


class BasisQueryOperations(Generic[M, I, E, O]):

    model: type[M]
    input_scheme: type[I]
    edit_schema: type[E]
    out_scheme: type[O]

    async def query(self, session: AsyncSession, query: Select) -> Result:
        _log.info("Query %s", self.model.__name__)

        result = await session.execute(query)
        return result
