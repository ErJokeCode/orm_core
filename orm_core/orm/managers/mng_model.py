import logging
from typing import Any, Literal, Optional, Sequence, TypeVar, Generic, Union, overload
from uuid import UUID
from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import Result, Select, asc, delete, desc, func, inspect, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..basic_operations.model.add import BasicModelAddOperations
from ..basic_operations.model.get_all import BasicModelGetAllOperations
from ..basic_operations.model.edit import BasicModelEditOperations
from ..basic_operations.model.delete import BasicModelDeleteOperations


_log = logging.getLogger(__name__)


M = TypeVar('M')


# class BasicModelGetByOperations наследуется из BasicModelEditOperations
class MngModel(
    BasicModelAddOperations[M],
    BasicModelGetAllOperations[M],
    BasicModelEditOperations[M],
    BasicModelDeleteOperations[M],
    Generic[M]
):
    """
    Менеджер для работы с моделями

    Args:
        BasicModelAddOperations (_type_): Работа с добавлением
        BasicModelGetAllOperations (_type_): Работа с получением всех объектов
        BasicModelEditOperations (_type_): Работа с редактированием и получением по id и полям
        BasicModelDeleteOperations (_type_): Работа с удалением
        Generic (_type_): _type_
    """

    def __init__(self, model: type[M]) -> None:
        self.model = model
