import logging
from typing import Any, Literal, Optional, Sequence, TypeVar, Generic, Union, overload
from fastapi import HTTPException
from sqlalchemy import Select, asc,  desc as func_desc, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from orm_core.base_schemes import ListDTO


_log = logging.getLogger(__name__)


M = TypeVar('M')


class BasicModelGetAllOperations(Generic[M]):

    model: type[M]

    @overload
    async def get_all(
        self,
        session: AsyncSession,
        *,
        search: str,
        search_fields: list[str],
        loads: Optional[dict[str, str]] = None,
        sort_by: str,
        desc: int,
        page: int = 1,
        limit: int = -1,
        is_pagination: Literal[False],
        **kwargs: Any
    ) -> Sequence[M]:
        ...

    @overload
    async def get_all(
        self,
        session: AsyncSession,
        *,
        search: str,
        search_fields: list[str],
        loads: Optional[dict[str, str]] = None,
        sort_by: str,
        desc: int,
        page: int = 1,
        limit: int = -1,
        **kwargs: Any
    ) -> ListDTO[M]:
        ...

    @overload
    async def get_all(
        self,
        session: AsyncSession,
        *,
        search: str,
        search_fields: list[str],
        loads: Optional[dict[str, str]] = None,
        page: int = 1,
        limit: int = -1,
        is_pagination: Literal[False],
        **kwargs: Any
    ) -> Sequence[M]:
        ...

    @overload
    async def get_all(
        self,
        session: AsyncSession,
        *,
        search: str,
        search_fields: list[str],
        loads: Optional[dict[str, str]] = None,
        page: int = 1,
        limit: int = -1,
        **kwargs: Any
    ) -> ListDTO[M]:
        ...

    @overload
    async def get_all(
        self,
        session: AsyncSession,
        *,
        query_select: Optional[Select[Any]],
        sort_by: str,
        desc: int,
        page: int = 1,
        limit: int = -1,
        is_pagination: Literal[False],
        **kwargs: Any
    ) -> Sequence[M]:
        ...

    @overload
    async def get_all(
        self,
        session: AsyncSession,
        *,
        query_select: Optional[Select[Any]],
        sort_by: str,
        desc: int,
        page: int = 1,
        limit: int = -1,
        **kwargs: Any
    ) -> ListDTO[M]:
        ...

    @overload
    async def get_all(
        self,
        session: AsyncSession,
        *,
        query_select: Optional[Select[Any]],
        page: int = 1,
        limit: int = -1,
        is_pagination: Literal[False],
        **kwargs: Any
    ) -> Sequence[M]:
        ...

    @overload
    async def get_all(
        self,
        session: AsyncSession,
        *,
        query_select: Optional[Select[Any]],
        page: int = 1,
        limit: int = -1,
        **kwargs: Any
    ) -> ListDTO[M]:
        ...

    @overload
    async def get_all(
        self,
        session: AsyncSession,
        *,
        loads: Optional[dict[str, str]] = None,
        page: int = 1,
        limit: int = -1,
        is_pagination: Literal[False],
        **kwargs: Any
    ) -> Sequence[M]:
        ...

    @overload
    async def get_all(
        self,
        session: AsyncSession,
        *,
        loads: Optional[dict[str, str]] = None,
        page: int = 1,
        limit: int = -1,
        **kwargs: Any
    ) -> ListDTO[M]:
        ...

    async def get_all(
        self,

        session: AsyncSession,

        search: Optional[str] = None,

        search_fields: Optional[list[str]] = None,

        loads: Optional[dict[str, str]] = None,

        sort_by: Optional[str] = None,

        query_select: Optional[Select[Any]] = None,

        desc: int = 0,

        page: int = 1,

        limit: int = -1,

        is_pagination: bool = True,

        **kwargs: Any

    ) -> Union[ListDTO[M], Sequence[M]]:

        _log.debug("Get all model %s", self.model.__name__)

        desc_int = desc

        if query_select is None:
            query_select = select(
                self.model
            )

        if search and search_fields:
            search_conditions = []
            for field in search_fields:
                if hasattr(self.model, field):
                    column = getattr(self.model, field)
                    search_conditions.append(  # type: ignore
                        column.ilike(f"%{search}%"))  # type: ignore

            if search_conditions:
                query_select = query_select.filter(
                    or_(*search_conditions))  # type: ignore

        if loads:
            for key, val in loads.items():
                if val == "s":
                    query_select = query_select.options(
                        selectinload(getattr(self.model, key))
                    )
                elif val == "j":
                    query_select = query_select.options(
                        joinedload(getattr(self.model, key))
                    )

        if kwargs:
            query_select = query_select.filter_by(**kwargs)

        if page < 1:
            raise HTTPException(
                status_code=400, detail="Page number must be greater than 0"
            )

        q_total_record = query_select

        if sort_by:
            query_select = query_select.order_by(
                func_desc(getattr(self.model, sort_by)) if desc_int else asc(
                    getattr(self.model, sort_by))
            )

        query_select = query_select.offset((page - 1) * limit)
        if limit != -1:
            query_select = query_select.limit(limit)

        result = await session.execute(query_select)
        content = result.scalars().all()

        if is_pagination:
            q_total_record = q_total_record.with_only_columns(
                func.count(self.model.id))  # type: ignore
            r_total_record = await session.execute(q_total_record)
            total_record = r_total_record.scalar_one_or_none()

            if total_record is None:
                total_record = 0

            if limit == -1:
                pages = 1
            else:
                pages = total_record // limit if total_record % limit == 0 else total_record // limit + 1

            return ListDTO[M](
                page_number=page,
                page_size=limit if limit != -1 else total_record,
                total_pages=pages,
                total_record=total_record,
                content=[item for item in content]
            )
        else:
            return content
