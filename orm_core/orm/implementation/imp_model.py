import logging
from typing import Any, Literal, Optional, Sequence, TypeVar, Generic, Union, overload
from uuid import UUID
from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import Result, Select, asc, delete, desc, func, inspect, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..basic_operations.basic_operation_get import BasicGetOperations
from ..basic_operations.basic_operation_add import BasicAddOperations


_log = logging.getLogger(__name__)


M = TypeVar('M')


class ImpModel(
    BasicGetOperations,
    BasicAddOperations,
    Generic[M]
):
    def __init__(self, model: type[M]) -> None:
        self.model = model
