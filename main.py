from contextlib import asynccontextmanager
from fastapi import FastAPI

from database import db_helper
from models import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)


if __name__ == '__main__':
    import uvicorn


    uvicorn.run('main:app', reload=True)
