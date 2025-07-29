import logging
from typing import Any, Literal, Optional, TypeVar, Generic, Union, overload
from pydantic import BaseModel
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession

from ..model.add import BasicModelAddOperations


_log = logging.getLogger(__name__)


M = TypeVar('M')
A = TypeVar('A', bound=BaseModel, default=Any)
E = TypeVar('E', bound=BaseModel, default=Any)
O = TypeVar('O', bound=BaseModel, default=Any)


class BasicAddSchemeOperations(BasicModelAddOperations[M], Generic[M, A, E, O]):

    model: type[M]
    input_scheme: type[A]
    edit_scheme: type[E]
    out_scheme: type[O]

    pks: list[str]
    loads: dict[str, str]

    @overload
    async def add(
        self,

        *,

        session: AsyncSession,

        data: Union[A, M, dict[str, Any]],

        is_return: bool,

        is_model: bool,

        loads: Optional[dict[str, str]],

        query: Union[Select[Any], None]

    ) -> Union[M, O, None]: ...

    @overload
    async def add(
        self,

        *,

        session: AsyncSession,

        data: Union[A, M, dict[str, Any]],

        is_return: Literal[True] = True,

        is_model: Literal[True] = True,

        loads: Optional[dict[str, str]] = None,

        query: Union[Select[Any], None] = None

    ) -> M: ...

    @overload
    async def add(
        self,

        *,

        session: AsyncSession,

        data: Union[A, M, dict[str, Any]],

        is_return: Literal[True] = True,

        is_model: Literal[False] = False,

        loads: Optional[dict[str, str]] = None,

        query: Union[Select[Any], None] = None

    ) -> O: ...

    @overload
    async def add(
        self,

        *,

        session: AsyncSession,

        data: Union[A, M, dict[str, Any]],

        is_return: Literal[False] = False

    ) -> None: ...

    async def add(
        self,

        *,

        session: AsyncSession,

        data: Union[A, M, dict[str, Any]],

        is_return: bool = True,

        is_model: bool = True,

        loads: Optional[dict[str, str]] = None,

        query: Union[Select[Any], None] = None

    ) -> Union[M, O, None]:
        """Создание объекта

        Args:
            session (AsyncSession): Сессия
            data (Union[A, M, dict[str, Any]]): Данные для создания
            is_return (bool, optional): Возвращать ли объект. Defaults to True.
            is_model (bool, optional): Возвращать ли модель. Defaults to True.
            loads (Optional[dict[str, str]], optional): Список полей для загрузки связанных объектов. Defaults to None.
            query (Union[Select[Any], None], optional): Кастомный запрос для возврата. Defaults to None.

        Returns:
            Union[M, O, None]: Добавленный объект
        """

        _log.info("Add %s", self.model.__name__)

        if isinstance(data, self.model):
            model = data
        elif isinstance(data, dict):
            model = self.model(**data)
        else:
            model = self.model(**data.model_dump())  # type: ignore

        if loads is None and not is_model:
            loads = self.loads

        return_model = await super().add(
            session=session,
            data=model,
            is_return=is_return,
            loads=loads,
            query=query
        )

        if not is_return:
            return None

        if is_model:
            return return_model

        return self.out_scheme.model_validate(return_model)
