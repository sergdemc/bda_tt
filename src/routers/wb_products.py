from fastapi import APIRouter, HTTPException, Depends

from src.schemas import ProductCreateScheme, ProductResponseScheme, ProductRequestScheme
from src.db import get_async_session, AsyncSession
from src.services.wildberries import fetch_product_data
from src.repositories.products import ProductRepository

router = APIRouter(tags=['Products'])


@router.post(
    "/products",
    response_model=ProductResponseScheme,
    status_code=201,
    name='create_product',
)
async def create_product(
        data: ProductRequestScheme,
        db: AsyncSession = Depends(get_async_session),
):
    repo = ProductRepository(db)

    try:
        product: ProductCreateScheme | dict = await fetch_product_data(artikul=data.artikul)
        if isinstance(product, dict):
            raise ValueError
        db_product = await repo.create_product(product.model_dump())
        return ProductResponseScheme.from_orm(db_product)

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unhandled error: {str(e)}")


@router.get(
    "/products/{artikul}",
    response_model=ProductResponseScheme,
    status_code=200,
    name='get_product',
)
async def get_product(artikul: int, db: AsyncSession = Depends(get_async_session)):
    repo = ProductRepository(db)

    try:
        product = await repo.get_product_by_artikul(artikul)
        if not product:
            raise ValueError(f"Product with artikul {artikul} not found.")
        return ProductResponseScheme.from_orm(product)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# @router.get("/subscribe/{artikul}")
# async def subscribe_product(artikul: int, db: AsyncSession = Depends(get_async_session)):
#     """
#     Эндпоинт для подписки на обновление товара каждые 30 минут.
#     """
#     try:
#         await schedule_subscription(artikul=artikul, db=db)
#         return {"message": f"Subscription for product {artikul} started."}
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))
