from contextlib import asynccontextmanager
from fastapi import FastAPI
from persistance import (
    create_db_and_tables,
)
from promotion_controller import router as promotion_router
from dependencies import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating database tables")
    create_db_and_tables(engine)
    yield
    print("Disposing engine")
    engine.dispose()


app = FastAPI(lifespan=lifespan)


app.include_router(promotion_router)
