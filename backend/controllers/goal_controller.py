from collections.abc import Callable

from fastapi import APIRouter, Body, Depends, Query

from backend.auth import get_current_user
from backend.business_logic.services.interfaces import IGoalService
from backend.controllers.requests import GoalCreateRequest


def create_router(get_service: Callable[[], IGoalService]) -> APIRouter:
    router = APIRouter(prefix="/goals", tags=["Goals"])

    @router.get("/options")
    def options(
        service: IGoalService = Depends(get_service),
    ):
        return service.get_goal_options()

    @router.post("/set")
    def set_goal(
        payload: GoalCreateRequest = Body(...),
        current_user: str = Depends(get_current_user),
        service: IGoalService = Depends(get_service),
    ):
        return service.set_goal(current_user, payload.goal_code)

    @router.get("/user")
    def user_goal(
        current_user: str = Depends(get_current_user),
        service: IGoalService = Depends(get_service),
    ):
        return service.get_user_goal(current_user)

    @router.get("/resources")
    def goal_resources(
        goal_code: str = Query(..., min_length=1),
        current_user: str = Depends(get_current_user),
        service: IGoalService = Depends(get_service),
    ):
        return service.get_goal_resources(goal_code)

    @router.get("/recommendations")
    def habit_recommendations(
        goal_code: str = Query(..., min_length=1),
        level: str = Query(default="beginner"),
        current_user: str = Depends(get_current_user),
        service: IGoalService = Depends(get_service),
    ):
        return service.get_habit_recommendations(goal_code, level)

    return router


def create_goal_router(get_service: Callable[[], IGoalService]) -> APIRouter:
    return create_router(get_service)
