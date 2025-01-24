from fastapi import APIRouter, HTTPException, Depends

from services.subscription import SubscriptionService
from db import get_async_session, AsyncSession
from scheduler import scheduler

router = APIRouter(prefix='/subscribe', tags=['Subscriptions'])


def get_subscription_service() -> SubscriptionService:
    return SubscriptionService(scheduler=scheduler)


@router.get(
    '/{artikul}',
    response_model=dict,
    status_code=201,
    name='subscribe_to_product'
)
async def subscribe_to_product(
        artikul: int,
        subscription_service: SubscriptionService = Depends(get_subscription_service)
):
    if subscription_service.is_subscribed(artikul):
        raise HTTPException(status_code=400, detail=f"Already subscribed to artikul {artikul}")

    subscription_service.subscribe(artikul=artikul)

    return {"msg": f"Subscribed to updates for artikul {artikul} every 30 minutes."}


@router.delete(
    '/{artikul}',
    response_model=dict,
    status_code=200,
    name='unsubscribe_from_product',
)
async def unsubscribe_from_product(
        artikul: int,
        subscription_service: SubscriptionService = Depends(get_subscription_service)
):
    try:
        subscription_service.unsubscribe(artikul)
        return {"msg": f"Unsubscribed from updates for artikul {artikul}."}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
