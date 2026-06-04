from collections.abc import Callable

from fastapi import APIRouter, Depends, HTTPException
from backend.auth import get_current_user
from backend.business_logic.services.interfaces import IGroupService
from backend.controllers.requests import GroupCreateRequest, GroupJoinRequest


def create_router(get_service: Callable[[], IGroupService]) -> APIRouter:
    router = APIRouter(prefix="/groups", tags=["Groups"])

    @router.get("/")
    def all_groups(
        service: IGroupService = Depends(get_service),
    ):
        return service.get_groups()

    @router.post("/create")
    def create(
        payload: GroupCreateRequest,
        current_user: str = Depends(get_current_user),
        service: IGroupService = Depends(get_service),
    ):
        return service.create_group(payload.name)

    @router.post("/join")
    def join(
        payload: GroupJoinRequest,
        current_user: str = Depends(get_current_user),
        service: IGroupService = Depends(get_service),
    ):
        joined = service.join_group(payload.group_id, payload.user_id)
        if not joined:
            raise HTTPException(status_code=404, detail="Group not found")
        return {"message": "Joined group"}

    return router
