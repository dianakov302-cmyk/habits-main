from collections.abc import Callable

from fastapi import APIRouter, Depends
from backend.auth import get_current_user
from backend.business_logic.services.interfaces import IChallengeService
from backend.controllers.requests import (
    ChallengeCreateRequest,
    ChallengeUpdateRequest,
    ChallengeRegisterRequest,
    ChallengeSubmitProofRequest,
    ChallengeModerateRequest,
)


def create_router(get_service: Callable[[], IChallengeService]) -> APIRouter:
    router = APIRouter(prefix="/challenges", tags=["Challenges"])

    @router.get("/")
    def all_challenges(
        service: IChallengeService = Depends(get_service),
    ):
        return service.get_challenges()

    @router.post("/create")
    def create(
        payload: ChallengeCreateRequest,
        current_user: str = Depends(get_current_user),
        service: IChallengeService = Depends(get_service),
    ):
        return service.create_challenge(payload.title)

    @router.put("/{challenge_id}")
    def update_challenge(
        challenge_id: str,
        payload: ChallengeUpdateRequest,
        current_user: str = Depends(get_current_user),
        service: IChallengeService = Depends(get_service),
    ):
        updates = payload.model_dump(exclude_none=True)
        return service.update_challenge(challenge_id, updates)

    @router.delete("/{challenge_id}")
    def delete_challenge(
        challenge_id: str,
        current_user: str = Depends(get_current_user),
        service: IChallengeService = Depends(get_service),
    ):
        return service.delete_challenge(challenge_id)

    @router.post("/{challenge_id}/register")
    def register(
        challenge_id: str,
        payload: ChallengeRegisterRequest,
        current_user: str = Depends(get_current_user),
        service: IChallengeService = Depends(get_service),
    ):
        return service.register_for_challenge(challenge_id, payload.user_email)

    @router.get("/{challenge_id}/leaderboard")
    def leaderboard(
        challenge_id: str,
        current_user: str = Depends(get_current_user),
        service: IChallengeService = Depends(get_service),
    ):
        return service.get_leaderboard(challenge_id)

    @router.post("/{challenge_id}/submit")
    def submit_proof(
        challenge_id: str,
        payload: ChallengeSubmitProofRequest,
        current_user: str = Depends(get_current_user),
        service: IChallengeService = Depends(get_service),
    ):
        return service.submit_proof(
            challenge_id, payload.user_email, payload.day, payload.proof_url
        )

    @router.get("/{challenge_id}/submissions")
    def get_submissions(
        challenge_id: str,
        current_user: str = Depends(get_current_user),
        service: IChallengeService = Depends(get_service),
    ):
        return service.get_submissions(challenge_id)

    @router.put("/{challenge_id}/submissions/{submission_id}")
    def moderate_submission(
        challenge_id: str,
        submission_id: str,
        payload: ChallengeModerateRequest,
        current_user: str = Depends(get_current_user),
        service: IChallengeService = Depends(get_service),
    ):
        return service.moderate_submission(submission_id, payload.status)

    return router
