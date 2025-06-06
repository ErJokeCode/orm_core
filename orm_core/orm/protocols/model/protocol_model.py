from typing import (
    Generic, Optional, TypeVar, Protocol, overload, Literal, Any
)

from .pr_md_get import ModelGetProtocol
from .pr_md_add import ModelAddProtocol

M = TypeVar('M')


class ModelProtocal(ModelAddProtocol[M], ModelGetProtocol[M], Protocol):

    def __init__(self, model: type[M]) -> None:
        raise NotImplementedError
