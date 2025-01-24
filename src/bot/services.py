import httpx


async def fetch_product_from_api(artikul: int, api_url: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{api_url}/api/v1/products/{artikul}")
        if response.status_code == 200:
            return response.json()
        return {"error": f"Failed to fetch product data: {response.status_code}"}
