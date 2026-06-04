from collections.abc import Callable

from fastapi import APIRouter, Depends

from backend.auth import get_current_user
from backend.business_logic.services.interfaces import IWeeklyReviewService
from backend.controllers.requests import WeeklyReviewSubmitRequest


def create_router(get_service: Callable[[], IWeeklyReviewService]) -> APIRouter:
    router = APIRouter(prefix="/reviews", tags=["Weekly Reviews"])

    @router.post("/submit")
    def submit_review(
        payload: WeeklyReviewSubmitRequest,
        current_user: str = Depends(get_current_user),
        service: IWeeklyReviewService = Depends(get_service),
    ):
        return service.submit_review(
            current_user,
            payload.what_worked,
            payload.what_distracted,
            payload.what_to_change,
        )

    @router.get("/history")
    def get_history(
        current_user: str = Depends(get_current_user),
        service: IWeeklyReviewService = Depends(get_service),
    ):
        return service.get_history(current_user)

    @router.get("/latest")
    def get_latest(
        current_user: str = Depends(get_current_user),
        service: IWeeklyReviewService = Depends(get_service),
    ):
        return service.get_latest(current_user)

    return router
