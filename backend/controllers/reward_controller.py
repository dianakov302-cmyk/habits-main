from collections.abc import Callable

from fastapi import APIRouter, Depends

from backend.auth import get_current_user
from backend.business_logic.services.interfaces import IRewardService
from backend.controllers.requests import RewardCheckRequest, RewardActivateRequest


def create_router(get_service: Callable[[], IRewardService]) -> APIRouter:
    router = APIRouter(prefix="/rewards", tags=["Rewards"])

    @router.get("/catalog")
    def get_catalog(
        current_user: str = Depends(get_current_user),
        service: IRewardService = Depends(get_service),
    ):
        return service.get_catalog()

    @router.get("/user")
    def get_user_rewards(
        current_user: str = Depends(get_current_user),
        service: IRewardService = Depends(get_service),
    ):
        return service.get_user_rewards(current_user)

    @router.post("/check-unlock")
    def check_and_unlock(
        payload: RewardCheckRequest,
        current_user: str = Depends(get_current_user),
        service: IRewardService = Depends(get_service),
    ):
        return service.check_and_unlock(
            current_user,
            payload.current_streak,
            payload.completed_programs,
            payload.weekly_reviews,
        )

    @router.post("/activate")
    def activate(
        payload: RewardActivateRequest,
        current_user: str = Depends(get_current_user),
        service: IRewardService = Depends(get_service),
    ):
        return service.activate_reward(current_user, payload.reward_code)

    return router
