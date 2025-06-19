import logging
from typing import Any, Literal, Optional,  TypeVar, Generic,  overload
from fastapi import HTTPException
from sqlalchemy import Select, select
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession


_log = logging.getLogger(__name__)


M = TypeVar('M')


class BasicModelEditOperations(Generic[M]):

    model: type[M]

    @overload
    async def edit(
        self,
        *,
        session: AsyncSession,
        edit_item: dict[str, Any],
        get_return: Literal[False],
        **pks: Any
    ) -> None: ...

    @overload
    async def edit(
        self,
        *,
        session: AsyncSession,
        edit_item: dict[str, Any],
        return_query: Select[Any],
        is_get_none: Literal[False],
        **pks: Any
    ) -> M: ...

    @overload
    async def edit(
        self,
        *,
        session: AsyncSession,
        edit_item: dict[str, Any],
        return_query: Select[Any],
        **pks: Any
    ) -> Optional[M]: ...

    async def edit(
        self,

        *,

        session: AsyncSession,

        edit_item: dict[str, Any],

        loads: Optional[dict[str, str]] = None,

        is_return: bool = True,

        return_query: Optional[Select[Any]] = None,

        is_get_none: bool = True,

        **pks: Any

    ) -> Optional[M]:

        _log.info("Edit model %s", self.model.__name__)

        stmt = select(self.model).filter_by(**pks)

        if loads is not None:
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
        model = r.scalars().first()

        if model is None:
            raise HTTPException(
                status_code=404, detail=f"{self.model.__name__} not found")

        for key, value in edit_item.items():
            if value is not None:
                setattr(model, key, value)

        await session.flush()

        if not is_return:
            return None

        if return_query is None:
            return model

        stmt = return_query.filter_by(**pks)

        r = await session.execute(stmt)
        model = r.scalars().first()

        if model is not None:
            return model

        if is_get_none:
            return None

        raise HTTPException(
            status_code=404, detail=f"{self.model.__name__} not found")
