from enum import Enum
from typing import Any, Generic, Optional, Sequence, TypeVar, Union, overload

from fastapi import APIRouter, params
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

from orm_core.api.base_api import BaseApi
from orm_core.orm.model_orm import BaseModelOrm

M = TypeVar('M')
A = TypeVar('A', bound=BaseModel, default=Any)
E = TypeVar('E', bound=BaseModel, default=Any)
O = TypeVar('O', bound=BaseModel, default=Any)


class ItemOrm(BaseModelOrm, Generic[M, A, E, O]):
    """
    ORM класс для работы с моделью.

    При инициализации только с model и схемами не создает роутер.
    При передаче session_factory и search_fields создает роутер FastAPI.

    Примеры:
        # Без роутера
        item = ItemOrm(MyModel, InputScheme, EditScheme, OutputScheme)
        hasattr(item, 'router')  # False

        # С роутером
        item = ItemOrm(MyModel, InputScheme, EditScheme, OutputScheme, 
                      ["name"], session_factory)
        hasattr(item, 'router')  # True
        isinstance(item.router, APIRouter)  # True
    """

    @overload
    def __init__(
        self,
        model: type[M],
        input_scheme: type[A],
        edit_scheme: type[E],
        out_scheme: type[O],
    ) -> None:
        '''
        При инициализации только с model и схемами не создает роутер.
        Пример:
        item = ItemOrm(MyModel, InputScheme, EditScheme, OutputScheme)
        hasattr(item, 'router')  # False
        '''
        ...

    @overload
    def __init__(
        self,
        model: type[M],
        input_scheme: type[A],
        edit_scheme: type[E],
        out_scheme: type[O],
        *,
        search_fields: list[str],
        session_factory: async_sessionmaker[AsyncSession]
    ) -> None:
        '''
        При передаче session_factory и search_fields создает роутер FastAPI.
        Пример:
        item = ItemOrm(MyModel, InputScheme, EditScheme, OutputScheme, 
                      ["name"], session_factory)
        hasattr(item, 'router')  # True
        isinstance(item.router, APIRouter)  # True
        '''
        ...

    @overload
    def __init__(
        self,
        model: type[M],
        input_scheme: type[A],
        edit_scheme: type[E],
        out_scheme: type[O],
        *,
        search_fields: list[str],
        session_factory: async_sessionmaker[AsyncSession],
        prefix: Optional[str] = None,
        tags: Optional[list[Union[str, Enum]]] = None,
        dependencies: Optional[Sequence[params.Depends]] = None,
    ) -> None:
        '''
        Дополнительные параметры для создания роутера FastAPI.
        '''
        ...

    def __init__(
        self,
        model: type[M],
        input_scheme: type[A],
        edit_scheme: type[E],
        out_scheme: type[O],
        search_fields: Union[list[str], None] = None,
        session_factory: Union[async_sessionmaker[AsyncSession], None] = None,
        prefix: Optional[str] = None,
        tags: Optional[list[Union[str, Enum]]] = None,
        dependencies: Optional[Sequence[params.Depends]] = None,
    ) -> None:
        super().__init__(model, input_scheme, edit_scheme, out_scheme)

        if session_factory is not None:
            self.__api_orm = BaseApi(
                self,
                session_factory,
                search_fields,
                prefix=prefix,
                tags=tags,
                dependencies=dependencies
            )

            self.__router = self.__api_orm.router

    @property
    def router(self) -> APIRouter:
        """FastAPI router associated with this ORM (available only if session_factory was provided)."""
        if self.__router is None:
            raise AttributeError(
                "Router is not available. Initialize ItemOrm with session_factory.")
        return self.__router
