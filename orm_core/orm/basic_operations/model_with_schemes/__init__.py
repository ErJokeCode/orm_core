from typing import Any, Generic, TypeVar

from pydantic import BaseModel

from .add import BasicAddSchemeOperations
from .get_by import BasicGetBySchemeOperations


M = TypeVar('M')
A = TypeVar('A', bound=BaseModel, default=Any)
E = TypeVar('E', bound=BaseModel, default=Any)
O = TypeVar('O', bound=BaseModel, default=Any)


class ManagerModelSchemes(
    BasicAddSchemeOperations[M, A, E, O],
    BasicGetBySchemeOperations[M, A, E, O],
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
