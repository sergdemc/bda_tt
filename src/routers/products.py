from fastapi import APIRouter, HTTPException, Depends

from src.schemas import ProductCreateScheme, ProductResponseScheme
from src.db import get_async_session, AsyncSession

router = APIRouter(tags=['Products'])


@router.post(
    "/products",
    response_model=ProductResponseScheme,
    status_code=201,
    name='create_product',
)
async def create_product(data: ProductCreateScheme, db: AsyncSession = Depends(get_async_session)):
    """
    Эндпоинт для сохранения товара в БД по артикулу.
    """
    try:
        product = await fetch_product_data(artikul=data.artikul, db=db)
        return product
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/products/{artikul}",
    response_model=ProductResponseScheme,
    status_code=200,
    name='get_product',
)
async def get_product(artikul: str, db: AsyncSession = Depends(get_async_session)):
    """
    Эндпоинт для получения товара из БД по артикулу.
    """
    try:
        product = await fetch_product_data(artikul=artikul, db=db)
        return product
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/api/v1/subscribe/{artikul}")
async def subscribe_product(artikul: int, db: AsyncSession = Depends(get_async_session)):
    """
    Эндпоинт для подписки на обновление товара каждые 30 минут.
    """
    try:
        await schedule_subscription(artikul=artikul, db=db)
        return {"message": f"Subscription for product {artikul} started."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
