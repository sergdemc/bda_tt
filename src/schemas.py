from pydantic import BaseModel


class ProductRequestScheme(BaseModel):
    artikul: int


class ProductCreateScheme(BaseModel):
    artikul: int
    name: str
    price: float
    rating: float
    stock_quantity: int


class ProductResponseScheme(BaseModel):
    id: int
    artikul: int
    name: str
    price: float
    rating: float
    stock_quantity: int
    updated_at: str

    class Config:
        orm_mode = True
