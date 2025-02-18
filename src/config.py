import os

from dotenv import load_dotenv

load_dotenv()

DB_USER: str | None = os.getenv('DB_USER')
DB_PASSWORD: str | None = os.getenv('DB_PASSWORD')
DB_HOST: str | None = os.getenv('DB_HOST')
DB_PORT: str | None = os.getenv('DB_PORT')
DB_NAME: str | None = os.getenv('DB_NAME')

PORT: int = int(os.getenv('PORT', 8000))

POSTGRES_URL: str = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
