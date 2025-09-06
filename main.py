from contextlib import asynccontextmanager
from fastapi import FastAPI

from api import router as api_router
from database import db_helper
from models import Base


app = FastAPI()
app.include_router(api_router)

if __name__ == '__main__':
    import uvicorn


    uvicorn.run('main:app', reload=True)
