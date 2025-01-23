from src.schemas import ProductCreateScheme
import httpx
from sqlalchemy.ext.asyncio import AsyncSession

WB_API_URL = "https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm={}"


async def fetch_product_data(artikul: int) -> ProductCreateScheme | dict:
    url = WB_API_URL.format(artikul)

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()  # Проверяем статус ответа (выбросит httpx.HTTPStatusError при ошибке)

        data = response.json()

        if not data.get("data") or not data["data"].get("products"):
            return {'msg': f"Product with artikul {artikul} not found."}

        product_data = data["data"]["products"][0]
        name = product_data["name"]
        price = product_data["price"] / 100
        rating = product_data["rating"]
        stock_quantity = sum(stock["qty"] for stock in product_data["sizes"][0]["stocks"])

        return ProductCreateScheme(
            artikul=artikul, name=name, price=price, rating=rating, stock_quantity=stock_quantity
        )

    except httpx.RequestError as e:
        raise RuntimeError(f"Network error occurred: {e}")
    except KeyError as e:
        raise ValueError(f"Invalid response format: missing key {e}")
    except Exception as e:
        raise RuntimeError(f"Unexpected error: {e}")


# async def schedule_subscription(artikul: int, db: AsyncSession):
#     """
#     Запуск задачи для обновления данных о товаре каждые 30 минут.
#     """
#
#     async def fetch_and_update():
#         await fetch_product_data(artikul=artikul, db=db)
#
#     scheduler.add_job(fetch_and_update, "interval", minutes=30, id=f"update_{artikul}")
