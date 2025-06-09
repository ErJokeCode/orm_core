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


class BasicModelAddOperations(Generic[M]):

    model: type[M]

    @overload
    async def add(
        self,
        *,
        session: AsyncSession,
        data: Union[M, dict]
    ) -> M:
        ...

    @overload
    async def add(
        self,
        *,
        session: AsyncSession,
        data: Union[M, dict],
        loads: dict[str, str]
    ) -> M:
        ...

    @overload
    async def add(
        self,
        *,
        session: AsyncSession,
        data: Union[M, dict],
        return_query: Select
    ) -> M:
        ...

    @overload
    async def add(
        self,
        *,
        session: AsyncSession,
        data: Union[M, dict],
        is_return: Literal[False] = False
    ) -> None:
        ...

    @overload
    async def add(
        self,
        *,
        session: AsyncSession,
        data: Union[M, dict],
        is_return: bool = True,
        loads: Optional[dict[str, str]] = None,
        return_query: Optional[Select] = None
    ) -> Optional[M]:
        ...

    async def add(
        self,

        *,

        session: AsyncSession,

        data: Union[M, dict],

        is_return: bool = True,

        loads: Optional[dict[str, str]] = None,

        return_query: Optional[Select] = None

    ) -> Optional[M]:

        _log.debug("Add model %s", self.model.__name__)

        if isinstance(data, dict):
            model: M = self.model(**data)
        else:
            model = data

        session.add(model)
        await session.flush()

        if not is_return:
            return None

        if loads:
            stmt = select(self.model).filter_by(
                id=model.id  # type: ignore
            )
            for key, val in loads.items():
                if val == "s":
                    stmt = stmt.options(
                        selectinload(getattr(self.model, key))
                    )
                elif val == "j":
                    stmt = stmt.options(
                        joinedload(getattr(self.model, key))
                    )

            r = await session.execute(stmt)
            return_model = r.scalars().first()

        if return_query is not None:
            return_query = return_query.filter_by(
                id=model.id  # type: ignore
            )
            r = await session.execute(return_query)
            return_model = r.scalars().first()

        if return_model is None:
            _log.warning("Model %s not add in table", self.model.__name__)
            raise HTTPException(
                status_code=500, detail=f"Model {self.model.__name__} not add in table")

        return return_model
