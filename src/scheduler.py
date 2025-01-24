from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

from config import POSTGRES_URL

jobstores = {
    "default": SQLAlchemyJobStore(url=POSTGRES_URL.replace('+asyncpg', ''))
}

scheduler = AsyncIOScheduler(jobstores=jobstores)


def start_scheduler():
    scheduler.start()
    print("Scheduler started.")
