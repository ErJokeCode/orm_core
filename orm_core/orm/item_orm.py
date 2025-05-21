from typing import Generic, TypeVar

from pydantic import BaseModel

from orm_core.orm.api_orm import BaseApiOrm
from orm_core.orm.model_orm import BaseModelOrm

M = TypeVar('M')
I = TypeVar('I', bound=BaseModel)
E = TypeVar('E', bound=BaseModel)
O = TypeVar('O', bound=BaseModel)


class ItemOrm(BaseModelOrm, Generic[M, I, E, O]):
    def __init__(self, model: type[M], input_scheme: type[I], edit_schema: type[E], out_scheme: type[O]) -> None:
        super().__init__(model, input_scheme, edit_schema, out_scheme)
        self.api_orm = BaseApiOrm(self)
        self.router = self.api_orm.router
