from enum import Enum
import inspect
from typing import Annotated, Any, Generic, Literal, Optional, Sequence, TypeVar, Union
from fastapi import APIRouter, Body, Depends, params
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession


from .basic_api import BasicApi
from ..basic_operations.model import ManagerModel


M = TypeVar('M')


class ManagerApiModel(
    ManagerModel[M],
    BasicApi,
    Generic[M],
):
    def __init__(
        self,

        model: type[M],

        session_factory: async_sessionmaker[AsyncSession],

        search_fields: Optional[list[str]] = None,

        return_get_all: Literal["pagination", "list"] = "pagination",

        prefix: Optional[str] = None,

        tags: Optional[list[Union[str, Enum]]] = None,

        dependencies: Optional[Sequence[params.Depends]] = None,
    ) -> None:

        super().__init__(
            model=model
        )

        prefix = prefix if prefix else f"/{self.model.__name__.lower()}"
        tags = tags if tags else [self.model.__name__]

        self.__router = APIRouter(
            prefix=prefix,
            tags=tags,
            dependencies=dependencies,
        )

        BasicApi.__init__(
            self=self,
            router=self.__router,
            session_factory=session_factory,
            search_fields=search_fields,
            return_get_all=return_get_all,
            prefix=prefix,
            tags=tags,
            dependencies=dependencies
        )

        self.__fill_router()

    def __fill_router(self) -> None:
        self.__create_add()

    def __create_add(self) -> None:
        self.__router.add_api_route(
            path="/",
            endpoint=self.__create_func_add(),
            methods=["POST"],
            response_model=self.type_cols
        )

    def __create_func_add(self):
        type_cols = self.type_cols

        async def add(
            session: Annotated[AsyncSession, Depends(self.get_db_session)],
            data: Any = Body(json_schema_extra=type_cols)
        ):
            model = await self.add(
                session=session,
                data=data
            )
            return self.model_to_dict(model)

        return add
