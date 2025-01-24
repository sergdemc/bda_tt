from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from models import Product


class ProductRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_product_by_artikul(self, artikul: int) -> Product | None:
        query = select(Product).where(Product.artikul == artikul)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def create_or_update(
            self, artikul: int, name: str, price: float, rating: float, stock_quantity: int
    ) -> Product:

        product = await self.get_product_by_artikul(artikul)
        if product:
            return await self.update_product(product, name, price, rating, stock_quantity)
        return await self.create_product(artikul, name, price, rating, stock_quantity)

    async def create_product(
            self, artikul: int, name: str, price: float, rating: float, stock_quantity: int
    ) -> Product:

        product = Product(
            artikul=artikul,
            name=name,
            price=price,
            rating=rating,
            stock_quantity=stock_quantity,
        )
        self.db.add(product)
        await self.db.commit()
        await self.db.refresh(product)
        return product

    async def update_product(
            self, product: Product, name: str, price: float, rating: float, stock_quantity: int
    ) -> Product:

        product.name = name
        product.price = price
        product.rating = rating
        product.stock_quantity = stock_quantity
        await self.db.commit()
        await self.db.refresh(product)
        return product

    async def delete_product(self, artikul: int) -> None:

        product = await self.get_product_by_artikul(artikul)

        if product:
            await self.db.delete(product)
            await self.db.commit()
