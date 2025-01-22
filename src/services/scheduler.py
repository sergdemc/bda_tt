




async def schedule_subscription(artikul: int, db: AsyncSession):
    """
    Запуск задачи для обновления данных о товаре каждые 30 минут.
    """

    async def fetch_and_update():
        await fetch_product_data(artikul=artikul, db=db)

    scheduler.add_job(fetch_and_update, "interval", minutes=30, id=f"update_{artikul}")