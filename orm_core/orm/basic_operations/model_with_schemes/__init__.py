import logging
from typing import Any, Generic, Optional, TypeVar

from pydantic import BaseModel
from sqlalchemy.orm import class_mapper

from .add import BasicAddSchemeOperations
from .get_by import BasicGetBySchemeOperations


_log = logging.getLogger(__name__)


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

        primary_key = self.model.__table__.primary_key  # type: ignore
        self.pks: list[str] = primary_key.columns.keys()  # type: ignore

        mapper = class_mapper(self.model)
        self.attrs_rel: dict[str, str] = {}

        for attr in mapper.relationships:
            self.attrs_rel[attr.key] = attr.direction.name

        schema = self.out_scheme.model_json_schema()
        self.attrs_out_scheme: Optional[list[str]] = schema.get(
            "required")
        if self.attrs_out_scheme is None:
            self.attrs_out_scheme = []

        self.loads: dict[str, str] = {}
        for key, val in self.attrs_rel.items():
            if key in self.attrs_out_scheme:
                if val == "MANYTOMANY" or val == "ONETOMANY":
                    self.loads[key] = "s"
                elif val == "MANYTOONE" or val == "ONETOONE":
                    self.loads[key] = "j"
