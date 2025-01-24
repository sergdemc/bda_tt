import datetime
from sqlalchemy import text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func

from db import Base


class BaseModel(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', NOW())"))
    updated_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', NOW())"),
        onupdate=func.now()
    )


class Product(BaseModel):
    __tablename__ = 'products'

    artikul: Mapped[int] = mapped_column(unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    rating: Mapped[float] = mapped_column(default=0.0, nullable=False)
    stock_quantity: Mapped[int] = mapped_column(nullable=False)
