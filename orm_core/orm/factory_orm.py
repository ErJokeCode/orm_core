import logging
from typing import Any, Literal, Optional, Sequence, TypeVar, Generic, Union, overload
from uuid import UUID
from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import Result, Select, asc, delete, desc, func, inspect, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from .protocols.model.protocol_model import ModelProtocal
from .implementation.imp_model import ImpModel


_log = logging.getLogger(__name__)


M = TypeVar('M')
I = TypeVar('I', bound=BaseModel)
E = TypeVar('E', bound=BaseModel)
O = TypeVar('O', bound=BaseModel)


class FactoryOrm(Generic[M, I, E, O]):

    @overload
    @classmethod
    def create(
        cls,
        model: type[M]
    ) -> ImpModel[M]:
        ...

    @overload
    @classmethod
    def create(
            cls,
            model: type[M],
            input_scheme: type[I],
            edit_schema: type[E],
            out_scheme: type[O],
    ) -> None:
        ...

    @classmethod
    def create(
            cls,
            model: type[M],
            input_scheme: Optional[type[I]] = None,
            edit_schema: Optional[type[E]] = None,
            out_scheme: Optional[type[O]] = None,
    ) -> Union[ImpModel[M], None]:
        if input_scheme and edit_schema and out_scheme:
            return None

        return ImpModel(model)
