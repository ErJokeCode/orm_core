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
) -> "MngModel[M]": ...


@overload
def create_factory_orm(
    model: type[M],
    add_scheme: type[A],
    edit_scheme: type[E],
    out_scheme: type[O],
) -> "MngModelWithSchemes[M, A, E, O]": ...


def create_factory_orm(

    model: type[M],

    add_scheme: Optional[type[A]] = None,

    edit_scheme: Optional[type[E]] = None,

    out_scheme: Optional[type[O]] = None,

) -> Union["MngModel[M]", "MngModelWithSchemes[M, A, E, O]"]:

    if add_scheme and edit_scheme and out_scheme:
        return MngModelWithSchemes(model, add_scheme, edit_scheme, out_scheme)

    return MngModel(model)
