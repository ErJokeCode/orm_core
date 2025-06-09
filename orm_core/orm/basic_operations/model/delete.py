import logging
from typing import Any, Literal, Optional, Sequence, TypeVar, Generic, Union, overload
from uuid import UUID
from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import Result, Select, asc, delete, desc, func, inspect, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from orm_core.base_schemes import ResponseStatus


_log = logging.getLogger(__name__)


M = TypeVar('M')


class BasicModelDeleteOperations(Generic[M]):

    model: type[M]

    async def delete(
        self,

        *,

        session: AsyncSession,

        id: UUID

    ) -> ResponseStatus:

        _log.info("Delete model %s", self.model.__name__)

        del_model = await session.get(self.model, id)

        if del_model is None:
            raise HTTPException(
                status_code=404, detail=f"{self.model.__name__} not found")

        await session.delete(del_model)

        await session.flush()

        return ResponseStatus()
