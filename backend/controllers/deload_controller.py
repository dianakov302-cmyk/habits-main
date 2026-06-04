from collections.abc import Callable

from fastapi import APIRouter, Depends

from backend.auth import get_current_user
from backend.business_logic.services.interfaces import IDeloadService
from backend.controllers.requests import DeloadCompleteRequest


def create_router(get_service: Callable[[], IDeloadService]) -> APIRouter:
    router = APIRouter(prefix="/deload", tags=["Deload"])

    @router.get("/status")
    def get_status(
        current_user: str = Depends(get_current_user),
        service: IDeloadService = Depends(get_service),
    ):
        return service.get_status(current_user)

    @router.post("/complete")
    def complete_deload(
        payload: DeloadCompleteRequest,
        current_user: str = Depends(get_current_user),
        service: IDeloadService = Depends(get_service),
    ):
        return service.complete_deload(current_user, payload.activity)

    @router.get("/history")
    def get_history(
        current_user: str = Depends(get_current_user),
        service: IDeloadService = Depends(get_service),
    ):
        return service.get_history(current_user)

    return router
