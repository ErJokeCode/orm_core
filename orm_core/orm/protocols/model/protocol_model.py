from typing import (
    Generic, Optional, TypeVar, Protocol, overload, Literal, Any
)

from .pr_md_add import ModelAddProtocol

M = TypeVar('M')


class ModelProtocol(
    ModelAddProtocol[M],
    Protocol[M]
):

    def __init__(self, model: type[M]) -> None:
        raise NotImplementedError
