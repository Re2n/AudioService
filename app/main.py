from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.v1.Token import token_router
from api.v1.User import user_router
from core.config.Database import db
from schemas.Base import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await db.dispose()


app = FastAPI(lifespan=lifespan)

app.include_router(user_router)
# app.include_router(token_router)
