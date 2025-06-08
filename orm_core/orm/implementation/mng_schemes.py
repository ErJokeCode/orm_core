import logging
from typing import Any, Literal, Optional, Sequence, TypeVar, Generic, Union, overload
from uuid import UUID
from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import Result, Select, asc, delete, desc, func, inspect, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..basic_operations.bs_op_schemes.sc_add import BasicAddSchemeOperations

from ..basic_operations.bs_op_model.md_add import BasicModelAddOperations


M = TypeVar('M')
A = TypeVar('A', bound=BaseModel, default=Any)
E = TypeVar('E', bound=BaseModel, default=Any)
O = TypeVar('O', bound=BaseModel, default=Any)


class MngSchemes(
    BasicAddSchemeOperations,
    Generic[M, A, E, O],
):
    def __init__(
        self,
        model: type[M],
        add_scheme: type[A],
        edit_scheme: type[E],
        out_scheme: type[O]
    ) -> None:
        self.model = model
        self.add_scheme = add_scheme
        self.edit_scheme = edit_scheme
        self.out_scheme = out_scheme

        self.model_operation = BasicModelAddOperations(model)
