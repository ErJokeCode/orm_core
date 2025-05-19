from functools import partial

from fastapi import APIRouter

from orm.item_orm import ItemOrm


class BaseApiOrm:
    def __init__(self) -> None:
        self.router = APIRouter()

    def _create_get_handler(self, item_orm: ItemOrm):
        async def handler(id: int):
            return await item_orm.get_by(id)
        return handler

    def _create_get_all_handler(self, item_orm: ItemOrm):
        async def handler():
            return await item_orm.get_all()
        return handler

    async def create_router(self, item_orm: ItemOrm) -> None:
        output = item_orm.out_scheme

        self.router.get("/{id}", response_model=output)(
            self._create_get_handler(item_orm)
        )

        self.router.get("/", response_model=list[output])(
            self._create_get_all_handler(item_orm)
        )
