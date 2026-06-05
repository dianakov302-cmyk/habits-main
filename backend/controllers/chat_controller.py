from collections.abc import Callable

from fastapi import APIRouter, Depends, Query

from backend.auth import get_current_user
from backend.business_logic.services.interfaces import IChatService
from backend.controllers.requests import (
    ChatStartDMRequest,
    ChatSendMessageRequest,
)


def create_router(get_service: Callable[[], IChatService]) -> APIRouter:
    router = APIRouter(prefix="/chat", tags=["Chat"])

    @router.get("/conversations")
    def get_conversations(
        current_user: str = Depends(get_current_user),
        service: IChatService = Depends(get_service),
    ):
        return service.get_conversations(current_user)

    @router.post("/conversations")
    def start_dm(
        payload: ChatStartDMRequest,
        current_user: str = Depends(get_current_user),
        service: IChatService = Depends(get_service),
    ):
        return service.start_dm(current_user, payload.recipient_email)

    @router.get("/conversations/{conversation_id}/messages")
    def get_messages(
        conversation_id: str,
        current_user: str = Depends(get_current_user),
        service: IChatService = Depends(get_service),
    ):
        return service.get_messages(conversation_id, current_user)

    @router.post("/conversations/{conversation_id}/messages")
    def send_message(
        conversation_id: str,
        payload: ChatSendMessageRequest,
        current_user: str = Depends(get_current_user),
        service: IChatService = Depends(get_service),
    ):
        return service.send_message(conversation_id, current_user, payload.content)

    @router.get("/search-users")
    def search_users(
        query: str = Query(..., min_length=2),
        current_user: str = Depends(get_current_user),
        service: IChatService = Depends(get_service),
    ):
        return service.search_users(query)

    return router
