import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import Product
from src.schemas import ProductResponseScheme
from src.services.scheduler import scheduler

WB_API_URL = "https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm={}"


async def fetch_product_data(artikul: int, db: AsyncSession) -> ProductResponseScheme:
    """
    Получение данных о товаре из Wildberries API и сохранение в БД.
    """
    url = WB_API_URL.format(artikul)
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != 200:
            raise ValueError(f"Failed to fetch product data for artikul {artikul}.")

        product_data = response.json()["data"]["products"][0]

        product = Product(
            artikul=product_data["id"],
            name=product_data["name"],
            price=product_data["price"] / 100,
            rating=product_data["rating"],
            stock_quantity=sum(stock["qty"] for stock in product_data["sizes"][0]["stocks"]),
        )

        # Сохранение в БД
        db.add(product)
        await db.commit()
        await db.refresh(product)

    return ProductResponseScheme.from_orm(product)
