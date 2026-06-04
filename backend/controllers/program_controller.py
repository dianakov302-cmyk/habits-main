from collections.abc import Callable

from fastapi import APIRouter, Depends

from backend.auth import get_current_user
from backend.business_logic.services.interfaces import IProgramService
from backend.controllers.requests import ProgramStartRequest, ProgramCompleteDayRequest


def create_router(get_service: Callable[[], IProgramService]) -> APIRouter:
    router = APIRouter(prefix="/program", tags=["30-Day Program"])

    @router.post("/start")
    def start_program(
        payload: ProgramStartRequest,
        current_user: str = Depends(get_current_user),
        service: IProgramService = Depends(get_service),
    ):
        return service.start_program(current_user, payload.goal_code, payload.level)

    @router.get("/status")
    def get_status(
        current_user: str = Depends(get_current_user),
        service: IProgramService = Depends(get_service),
    ):
        return service.get_status(current_user)

    @router.post("/complete-day")
    def complete_day(
        current_user: str = Depends(get_current_user),
        service: IProgramService = Depends(get_service),
    ):
        return service.complete_day(current_user)

    @router.get("/phases")
    def get_phases(
        current_user: str = Depends(get_current_user),
        service: IProgramService = Depends(get_service),
    ):
        return service.get_phases()

    return router
