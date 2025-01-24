from fastapi import APIRouter, HTTPException, Depends

from schemas import ProductCreateScheme, ProductResponseScheme, ProductRequestScheme
from db import get_async_session, AsyncSession
from services.wildberries import fetch_product_data
from repositories.products import ProductRepository

router = APIRouter(prefix='/products', tags=['Products'])


@router.post(
    '/',
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
        product: ProductCreateScheme = await fetch_product_data(artikul=data.artikul)

        db_product = await repo.create_or_update(**product.model_dump())
        db_product.updated_at = db_product.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        return ProductResponseScheme.from_orm(db_product)

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unhandled error: {str(e)}")


@router.get(
    '/{artikul}',
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
        product.updated_at = product.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        return ProductResponseScheme.from_orm(product)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
