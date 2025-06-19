import logging
from typing import Generic, TypeVar

from .add import BasicModelAddOperations
from .get_all import BasicModelGetAllOperations
from .get_by import BasicModelGetByOperations
from .edit import BasicModelEditOperations
from .delete import BasicModelDeleteOperations


_log = logging.getLogger(__name__)


M = TypeVar('M')


# class BasicModelGetByOperations наследуется из BasicModelEditOperations
class ManagerModel(
    BasicModelAddOperations[M],
    BasicModelGetAllOperations[M],
    BasicModelGetByOperations[M],
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
        BasicModelGetByOperations (_type_): Работа с получением по полям
        Generic (_type_): _type_
    """

    def __init__(self, model: type[M]) -> None:
        self.model = model
        self.pks = self.model.__table__.primary_key.columns.keys()  # type: ignore
