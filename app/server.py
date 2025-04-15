from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.persistance import (
    create_db_and_tables,
)
from app.controllers.promotion_controller import router as promotion_router
from app.controllers.business_controller import router as business_router
from app.dependencies import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating database tables")
    create_db_and_tables(engine)
    yield
    print("Disposing engine")
    engine.dispose()


app = FastAPI(lifespan=lifespan)


app.include_router(promotion_router)
app.include_router(business_router)
