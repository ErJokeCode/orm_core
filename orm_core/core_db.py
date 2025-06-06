from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine  # noqa

from orm_core.base import Base


class ClientDB:
    def __init__(self, async_url: str):
        self.__engine = create_async_engine(
            url=async_url
        )

        self.session_factory = async_sessionmaker(self.__engine)

    async def init_db(self):
        async with self.__engine.begin() as conn:
            await conn.run_sync(
                lambda sync_conn: Base.metadata.create_all(
                    sync_conn, checkfirst=True)
            )

    async def drop_tables(self):
        async with self.__engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
