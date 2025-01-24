import httpx

from schemas import ProductCreateScheme

WB_API_URL = "https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm={}"


async def fetch_product_data(artikul: int) -> ProductCreateScheme:
    url = WB_API_URL.format(artikul)

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()

        data = response.json()
        if not data.get("data") or not data["data"].get("products"):
            raise ValueError("Invalid response format: missing key 'data' or 'products'")

        product_data = data["data"]["products"][0]
        name = product_data["name"]
        price = product_data["priceU"] / 100
        rating = product_data["rating"]
        stock_quantity = product_data["totalQuantity"]

        return ProductCreateScheme(
            artikul=artikul, name=name, price=price, rating=rating, stock_quantity=stock_quantity
        )

    except httpx.RequestError as e:
        raise RuntimeError(f"Network error occurred: {e}")
    except KeyError as e:
        raise ValueError(f"Invalid response format: missing key {e}")
    except Exception as e:
        raise RuntimeError(f"Unexpected error: {e}")
