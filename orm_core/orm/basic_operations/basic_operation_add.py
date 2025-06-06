import logging
from typing import Any, Literal, Optional, Sequence, TypeVar, Generic, Union, overload
from uuid import UUID
from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import Result, Select, asc, delete, desc, func, inspect, or_, select
from sqlalchemy.ext.asyncio import AsyncSession


_log = logging.getLogger(__name__)


M = TypeVar('M')
I = TypeVar('I', bound=BaseModel)
E = TypeVar('E', bound=BaseModel)
O = TypeVar('O', bound=BaseModel)


class BasicAddOperations(Generic[M, I, E, O]):

    model: type[M]
    input_scheme: type[I]
    edit_schema: type[E]
    out_scheme: type[O]

    async def add(
        self,
        session: AsyncSession,
        data: I | M,
        is_return: bool = True,
        is_model: bool = True,
        return_query: Union[Select, None] = None
    ) -> Union[M, O, None]:
        _log.info("Add %s", self.model.__name__)

        if isinstance(data, self.model):
            model: M = data
        else:
            model = self.model(**data.model_dump())  # type: ignore
        session.add(model)
        await session.flush()

        if return_query is not None:
            return_query = return_query.filter(
                self.model.id == model.id  # type: ignore
            )
            r = await session.execute(return_query)
            model = r.scalars().first()  # type: ignore

        if not is_return:
            return None

        if is_model:
            return model

        return self.out_scheme.model_validate(model)
