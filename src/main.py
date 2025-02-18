from contextlib import asynccontextmanager

import asyncio
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.wb_products import router as products_router
from routers.subscriptions import router as subscription_router
from db import Base, async_engine
from config import PORT
from scheduler import scheduler, start_scheduler


async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def lifespan(app: FastAPI):
    start_scheduler()
    yield
    scheduler.shutdown()


app = FastAPI(
    title='API for getting info about product',
    description='Getting info about the product by its product number',
    version='1.0.0',
    openapi_url='/api/v1/openapi.json',
    redoc_url=None,
    lifespan=lifespan

)


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'],
    allow_headers=['*'],
)


app.include_router(products_router, prefix='/api/v1')
app.include_router(subscription_router, prefix='/api/v1')


async def main():
    await create_tables()


if __name__ == '__main__':
    asyncio.run(main())
    uvicorn.run('main:app', host='0.0.0.0', port=PORT, reload=True, workers=3)
