from enum import Enum
from functools import partial
import logging
from uuid import UUID

from fastapi import APIRouter, Depends, params
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import exc
from typing import Annotated, AsyncGenerator, Optional, Sequence, Union
from fastapi.exceptions import HTTPException

from orm_core.base_schemes import ListDTO, ResponseStatus
from orm_core.orm.model_orm import BaseModelOrm


_log = logging.getLogger(__name__)


class BaseApi:
    def __init__(
        self,

        item_orm: BaseModelOrm,

        session_factory: async_sessionmaker[AsyncSession],

        search_fields: Union[list[str], None] = None,

        prefix: Union[str, None] = None,

        tags: Union[list[Union[str, Enum]], None] = None,

        dependencies: Optional[Sequence[params.Depends]] = None,

    ) -> None:
        self.__relations = item_orm.get_all_relations()
        self.__session_factory = session_factory
        self.__search_fields = search_fields

        prefix = prefix if prefix is not None else f"/{item_orm.model.__name__.lower()}"
        tags = tags if tags is not None else [item_orm.model.__name__]

        self.__router = APIRouter(
            prefix=prefix,
            tags=tags,
            dependencies=dependencies,
        )

        self.__create_router(item_orm)

    async def get_db_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.__session_factory() as session:
            try:
                yield session
                await session.commit()
            except exc.SQLAlchemyError as error:
                await session.rollback()
                _log.error(error)
                raise HTTPException(status_code=500, detail="Database error")

            finally:
                await session.close()

    def __create_router(self, item_orm: BaseModelOrm) -> None:
        self.__create_get(item_orm)
        self.__create_post(item_orm)
        self.__create_patch(item_orm)
        self.__create_delete(item_orm)

    def __create_get(self, item_orm: BaseModelOrm):
        output = item_orm.out_scheme

        self.__router.add_api_route(
            path="/all",
            endpoint=self.__create_func_get_all(item_orm),
            methods=["GET"],
            response_model=ListDTO[output]
        )

        self.__router.add_api_route(
            path="/all_list",
            endpoint=self.__create_func_get_all_list(item_orm),
            methods=["GET"],
            response_model=list[output]
        )

        self.__router.add_api_route(
            path="/{id}",
            endpoint=self.__create_func_get_one(item_orm),
            methods=["GET"],
            response_model=output
        )

    def __create_post(self, item_orm: BaseModelOrm):
        self.__router.add_api_route(
            path="/",
            endpoint=self.__create_func_add(item_orm),
            methods=["POST"],
            response_model=item_orm.out_scheme
        )

    def __create_patch(self, item_orm: BaseModelOrm):
        self.__router.add_api_route(
            path="/{id}",
            endpoint=self.__create_func_edit(item_orm),
            methods=["PATCH"],
            response_model=item_orm.out_scheme
        )

    def __create_delete(self, item_orm: BaseModelOrm):
        self.__router.add_api_route(
            path="/{id}",
            endpoint=self.__create_func_delete(item_orm),
            methods=["DELETE"],
            response_model=ResponseStatus
        )

    def __create_func_get_one(self, item_orm: BaseModelOrm):
        async def get_by_id(
            session: Annotated[AsyncSession, Depends(self.get_db_session)],
            id: Union[int, UUID]
        ):
            return await item_orm.get_by(
                session=session,
                id=id,
                is_get_none=False,
                is_model=False
            )
        return get_by_id

    def __create_func_get_all(self, item_orm: BaseModelOrm):
        async def get_all(
            session: Annotated[AsyncSession, Depends(self.get_db_session)],
            search: Union[str, None] = None,
            sort_by: Union[str, None] = None,
            desc_int: int = 0,
            page: int = 1,
            limit: int = -1,
        ):
            return await item_orm.get_all(
                session=session,
                search=search,
                search_fields=self.__search_fields,
                sort_by=sort_by,
                desc_int=desc_int,
                page=page,
                limit=limit,
                is_pagination=True,
                is_model=False
            )
        return get_all

    def __create_func_get_all_list(self, item_orm: BaseModelOrm):
        async def get_all_list(
            session: Annotated[AsyncSession, Depends(self.get_db_session)],
            search: Union[str, None] = None,
            sort_by: Union[str, None] = None,
            desc_int: int = 0,
            page: int = 1,
            limit: int = -1,
        ):
            return await item_orm.get_all(
                session=session,
                search=search,
                search_fields=self.__search_fields,
                sort_by=sort_by,
                desc_int=desc_int,
                page=page,
                limit=limit,
                is_pagination=False,
                is_model=False
            )
        return get_all_list

    def __create_func_add(self, item_orm: BaseModelOrm):
        add_scheme = item_orm.input_scheme

        async def add(
            session: Annotated[AsyncSession, Depends(self.get_db_session)],
            data: add_scheme
        ):
            return await item_orm.add(
                session=session,
                data=data,
                is_model=False
            )
        return add

    def __create_func_edit(self, item_orm: BaseModelOrm):
        edit_scheme = item_orm.edit_scheme

        async def edit(
            session: Annotated[AsyncSession, Depends(self.get_db_session)],
            id: Union[int, UUID],
            data: edit_scheme
        ):
            return await item_orm.edit(
                session=session,
                id=id,
                edit_item=data,
                is_model=False
            )
        return edit

    def __create_func_delete(self, item_orm: BaseModelOrm):
        async def delete(
            session: Annotated[AsyncSession, Depends(self.get_db_session)],
            id: Union[int, UUID]
        ):
            return await item_orm.delete(
                session=session,
                id=id,
            )
        return delete

    @property
    def router(self) -> APIRouter:
        return self.__router
