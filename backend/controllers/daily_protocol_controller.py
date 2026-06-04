from collections.abc import Callable

from fastapi import APIRouter, Depends, Query

from backend.auth import get_current_user
from backend.business_logic.services.interfaces import IDailyProtocolService
from backend.controllers.requests import (
    DailyProtocolCreateRequest,
    DailyProtocolCompleteRequest,
)


def create_router(get_service: Callable[[], IDailyProtocolService]) -> APIRouter:
    router = APIRouter(prefix="/protocol", tags=["Daily Protocol"])

    @router.get("/today")
    def get_today(
        current_user: str = Depends(get_current_user),
        service: IDailyProtocolService = Depends(get_service),
    ):
        return service.get_today(current_user)

    @router.post("/create")
    def create_protocol(
        payload: DailyProtocolCreateRequest,
        current_user: str = Depends(get_current_user),
        service: IDailyProtocolService = Depends(get_service),
    ):
        return service.create_protocol(
            current_user,
            payload.date,
            payload.minimum_task,
            payload.target_task,
            payload.bonus_task,
        )

    @router.post("/complete-task")
    def complete_task(
        payload: DailyProtocolCompleteRequest,
        current_user: str = Depends(get_current_user),
        service: IDailyProtocolService = Depends(get_service),
    ):
        return service.complete_task(current_user, payload.date, payload.task_type)

    @router.get("/history")
    def get_history(
        days: int = Query(default=30, ge=1, le=90),
        current_user: str = Depends(get_current_user),
        service: IDailyProtocolService = Depends(get_service),
    ):
        return service.get_history(current_user, days)

    return router
