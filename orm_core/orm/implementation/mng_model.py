import logging
from typing import Any, Literal, Optional, Sequence, TypeVar, Generic, Union, overload
from uuid import UUID
from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import Result, Select, asc, delete, desc, func, inspect, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..basic_operations.bs_op_model.md_add import BasicModelAddOperations
from ..basic_operations.bs_op_model.md_get_all import BasicModelGetAllOperations
from ..protocols.model.protocol_model import ModelProtocol


_log = logging.getLogger(__name__)


M = TypeVar('M')


class MngModel(
    ModelProtocol,

    BasicModelAddOperations,
    BasicModelGetAllOperations,

    Generic[M]
):
    def __init__(self, model: type[M]) -> None:
        self.model = model
