from collections.abc import Callable

from fastapi import APIRouter, Depends, Query

from backend.auth import get_current_user
from backend.business_logic.services.interfaces import IProductivityService
from backend.controllers.requests import (
    WaterLogRequest,
    WaterGoalRequest,
    PlannerTaskCreateRequest,
    PlannerTaskUpdateRequest,
    SRCardCreateRequest,
    SRCardReviewRequest,
    BrainstormCreateRequest,
    BrainstormIdeaRequest,
)


def create_router(get_service: Callable[[], IProductivityService]) -> APIRouter:
    router = APIRouter(prefix="/productivity", tags=["Productivity"])

    # --- water tracker ---

    @router.get("/water")
    def get_water_log(
        date: str = Query(..., description="YYYY-MM-DD"),
        current_user: str = Depends(get_current_user),
        service: IProductivityService = Depends(get_service),
    ):
        return service.get_water_log(current_user, date)

    @router.post("/water/log")
    def log_water(
        payload: WaterLogRequest,
        current_user: str = Depends(get_current_user),
        service: IProductivityService = Depends(get_service),
    ):
        return service.log_water(current_user, payload.date, payload.amount_ml)

    @router.put("/water/goal")
    def update_water_goal(
        payload: WaterGoalRequest,
        current_user: str = Depends(get_current_user),
        service: IProductivityService = Depends(get_service),
    ):
        return service.update_water_goal(current_user, payload.goal_glasses)

    # --- planner ---

    @router.get("/planner")
    def get_planner(
        date: str = Query(..., description="YYYY-MM-DD"),
        current_user: str = Depends(get_current_user),
        service: IProductivityService = Depends(get_service),
    ):
        return service.get_planner_tasks(current_user, date)

    @router.post("/planner")
    def create_task(
        payload: PlannerTaskCreateRequest,
        current_user: str = Depends(get_current_user),
        service: IProductivityService = Depends(get_service),
    ):
        return service.create_planner_task(
            current_user,
            payload.date,
            payload.title,
            payload.description,
            payload.priority,
            payload.time_slot,
        )

    @router.put("/planner/{task_id}")
    def update_task(
        task_id: str,
        payload: PlannerTaskUpdateRequest,
        current_user: str = Depends(get_current_user),
        service: IProductivityService = Depends(get_service),
    ):
        updates = payload.model_dump(exclude_none=True)
        return service.update_planner_task(task_id, updates)

    @router.delete("/planner/{task_id}")
    def delete_task(
        task_id: str,
        current_user: str = Depends(get_current_user),
        service: IProductivityService = Depends(get_service),
    ):
        return service.delete_planner_task(task_id)

    @router.post("/planner/{task_id}/complete")
    def complete_task(
        task_id: str,
        current_user: str = Depends(get_current_user),
        service: IProductivityService = Depends(get_service),
    ):
        return service.complete_planner_task(task_id)

    # --- spaced repetition ---

    @router.get("/sr/cards")
    def get_cards(
        current_user: str = Depends(get_current_user),
        service: IProductivityService = Depends(get_service),
    ):
        return service.get_sr_cards(current_user)

    @router.get("/sr/review")
    def get_due_cards(
        current_user: str = Depends(get_current_user),
        service: IProductivityService = Depends(get_service),
    ):
        return service.get_sr_due(current_user)

    @router.post("/sr/cards")
    def create_card(
        payload: SRCardCreateRequest,
        current_user: str = Depends(get_current_user),
        service: IProductivityService = Depends(get_service),
    ):
        return service.create_sr_card(current_user, payload.deck, payload.front, payload.back)

    @router.post("/sr/cards/{card_id}/review")
    def review_card(
        card_id: str,
        payload: SRCardReviewRequest,
        current_user: str = Depends(get_current_user),
        service: IProductivityService = Depends(get_service),
    ):
        return service.review_sr_card(card_id, payload.ease)

    @router.delete("/sr/cards/{card_id}")
    def delete_card(
        card_id: str,
        current_user: str = Depends(get_current_user),
        service: IProductivityService = Depends(get_service),
    ):
        return service.delete_sr_card(card_id)

    # --- brainstorm ---

    @router.get("/brainstorm")
    def get_sessions(
        current_user: str = Depends(get_current_user),
        service: IProductivityService = Depends(get_service),
    ):
        return service.get_brainstorm_sessions(current_user)

    @router.post("/brainstorm")
    def create_session(
        payload: BrainstormCreateRequest,
        current_user: str = Depends(get_current_user),
        service: IProductivityService = Depends(get_service),
    ):
        return service.create_brainstorm_session(current_user, payload.title, payload.tags)

    @router.post("/brainstorm/{session_id}/ideas")
    def add_idea(
        session_id: str,
        payload: BrainstormIdeaRequest,
        current_user: str = Depends(get_current_user),
        service: IProductivityService = Depends(get_service),
    ):
        return service.add_brainstorm_idea(session_id, payload.content)

    @router.delete("/brainstorm/{session_id}")
    def delete_session(
        session_id: str,
        current_user: str = Depends(get_current_user),
        service: IProductivityService = Depends(get_service),
    ):
        return service.delete_brainstorm_session(session_id)

    return router
