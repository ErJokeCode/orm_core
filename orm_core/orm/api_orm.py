from functools import partial

from fastapi import APIRouter

from orm_core.orm.model_orm import BaseModelOrm


class BaseApiOrm:
    def __init__(self, item_orm: BaseModelOrm) -> None:
        self.__router = APIRouter(
            prefix=f"/{item_orm.model.__name__.lower()}",
            tags=[item_orm.model.__name__],
        )
        self.__create_router(item_orm)

    def __create_router(self, item_orm: BaseModelOrm) -> None:
        output = item_orm.out_scheme

        self.__router.get("/{id}", response_model=output)(
            self.__create_get_handler(item_orm)
        )

        self.__router.get("/", response_model=list[output])(
            self.__create_get_all_handler(item_orm)
        )

    def __create_get_handler(self, item_orm: BaseModelOrm):
        async def handler1(
            id: int
        ):
            return await item_orm.get_by(id)
        return handler1

    def __create_get_all_handler(self, item_orm: BaseModelOrm):
        async def handler():
            return await item_orm.get_all()
        return handler

    @property
    def router(self) -> APIRouter:
        return self.__router
