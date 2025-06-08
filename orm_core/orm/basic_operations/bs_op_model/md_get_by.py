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
