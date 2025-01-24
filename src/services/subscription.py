from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.base import JobLookupError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from services.wildberries import fetch_product_data
from repositories.products import ProductRepository
from config import POSTGRES_URL


def get_async_session(db_url: str):
    engine = create_async_engine(db_url)
    async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    return async_session()


async def fetch_and_save(artikul: int, db_url: str):
    async with get_async_session(db_url) as db:
        try:
            product_data = await fetch_product_data(artikul)
            product_repo = ProductRepository(db)
            await product_repo.create_or_update(**product_data.model_dump())
        except Exception as e:
            print(f"Error during scheduled job for artikul {artikul}: {e}")


class SubscriptionService:
    def __init__(self, scheduler: BackgroundScheduler):
        self.scheduler = scheduler

    def is_subscribed(self, artikul: int) -> bool:
        job_id = self._generate_job_id(artikul)
        return self.scheduler.get_job(job_id) is not None

    def subscribe(self, artikul: int):

        job_id = self._generate_job_id(artikul)

        self.scheduler.add_job(
            func=fetch_and_save,
            trigger="interval",
            minutes=30,
            id=job_id,
            replace_existing=True,
            kwargs={"artikul": artikul, "db_url": POSTGRES_URL},
        )

    def unsubscribe(self, artikul: int):

        job_id = self._generate_job_id(artikul)
        try:
            self.scheduler.remove_job(job_id)
        except JobLookupError:
            raise ValueError(f"No subscription found for artikul {artikul}")

    @staticmethod
    def _generate_job_id(artikul: int) -> str:
        return f"product_{artikul}"
