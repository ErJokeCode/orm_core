import logging
from typing import Any, Literal, Optional, Sequence, TypeVar, Generic, Union, overload
from uuid import UUID
from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import Result, Select, asc, delete, desc, func, inspect, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from .managers.mng_model import MngModel
from .managers.mng_schemes import MngModelWithSchemes


_log = logging.getLogger(__name__)


M = TypeVar('M')
A = TypeVar('A', bound=BaseModel, default=Any)
E = TypeVar('E', bound=BaseModel, default=Any)
O = TypeVar('O', bound=BaseModel, default=Any)


@overload
def create_factory_orm(
    model: type[M]
) -> "MngModel[M]":
    """Фабрика для создания менеджера для работы только с моделями

    Args:
        model (type[M]): Модель для работы

    Returns:
        MngModel[M]: Менеджер для работы с моделями


    Example:

    from orm_core import ClientDB
    from orm_core import create_factory_orm

    class YourClientDB(ClientDB):
        def __init__(self, async_url: str):
            super().__init__(async_url)

            self.user = create_factory_orm(User)

    db_client = YourClientDB(
        "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"
    )

    await db_client.user.add(...)
    await db_client.user.edit(...)
    await db_client.user.get_all(...)
    await db_client.user.get_by(...)
    await db_client.user.get_by_query(...)
    await db_client.user.delete(...)
    """
    ...


@overload
def create_factory_orm(
    model: type[M],
    add_scheme: type[A],
    edit_scheme: type[E],
    out_scheme: type[O],
) -> "MngModelWithSchemes[M, A, E, O]":
    """Фабрика для создания менеджера для работы с моделями и преобразование в pydantic-схемы

    Args:
        model (type[M]): Модель для работы
        add_scheme (type[A]): Pydantic-схема для добавления
        edit_scheme (type[E]): Pydantic-схема для редактирования
        out_scheme (type[O]): Pydantic-схема для вывода

    Returns:
        MngModelWithSchemes[M, A, E, O]: Менеджер для работы с моделями и преобразование в pydantic-схемы


    Example:

        from orm_core import ClientDB
        from orm_core import create_factory_orm

        class YourClientDB(ClientDB):
            def __init__(self, async_url: str):
                super().__init__(async_url)

                self.user = create_factory_orm(
                    User
                    InputScheme,
                    EditScheme,
                    OutputScheme
                )

        db_client = YourClientDB(
            "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"
        )

        await db_client.user.add(...)
        await db_client.user.edit(...)
        await db_client.user.get_all(...)
        await db_client.user.get_by(...)
        await db_client.user.get_by_query(...)
        await db_client.user.delete(...)
    """
    ...


def create_factory_orm(

    model: type[M],

    add_scheme: Optional[type[A]] = None,

    edit_scheme: Optional[type[E]] = None,

    out_scheme: Optional[type[O]] = None,

) -> Union["MngModel[M]", "MngModelWithSchemes[M, A, E, O]"]:

    if add_scheme and edit_scheme and out_scheme:
        return MngModelWithSchemes(model, add_scheme, edit_scheme, out_scheme)

    return MngModel(model)
