from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from settings import settings


class DatabaseHelper:
    def __init__(self, url: str):
        self.engine = create_async_engine(url=url)
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            expire_on_commit=False,
        )


db_helper = DatabaseHelper(
    url=settings.db_url,
)