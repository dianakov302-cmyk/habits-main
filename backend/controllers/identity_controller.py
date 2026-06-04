from collections.abc import Callable

from fastapi import APIRouter, Depends

from backend.auth import get_current_user
from backend.business_logic.services.interfaces import IIdentityService
from backend.controllers.requests import IdentityRecalculateRequest


def create_router(get_service: Callable[[], IIdentityService]) -> APIRouter:
    router = APIRouter(prefix="/identity", tags=["Identity"])

    @router.get("/profile")
    def get_profile(
        current_user: str = Depends(get_current_user),
        service: IIdentityService = Depends(get_service),
    ):
        return service.get_profile(current_user)

    @router.post("/recalculate")
    def recalculate(
        current_user: str = Depends(get_current_user),
        service: IIdentityService = Depends(get_service),
    ):
        return service.recalculate(current_user)

    return router
