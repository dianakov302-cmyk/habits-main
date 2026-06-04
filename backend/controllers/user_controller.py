from collections.abc import Callable

from fastapi import APIRouter, Body, Depends, Query

from backend.auth import create_access_token, get_current_user
from backend.business_logic.services.interfaces import IUserService
from backend.controllers.requests import (
    UserCredentialsRequest,
    UserLogoutRequest,
    UserProfileUpdateRequest,
    UserQuizResultRequest,
)


def create_router(get_service: Callable[[], IUserService]) -> APIRouter:
    router = APIRouter(prefix="/users", tags=["Users"])

    @router.post("/login")
    def login(
        payload: UserCredentialsRequest = Body(...),
        service: IUserService = Depends(get_service),
    ):
        result = service.login_user(payload.email, payload.password)
        if result.get("status") == "success":
            token = create_access_token(result["email"])
            return {
                "status": "success",
                "access_token": token,
                "token_type": "bearer",
                "email": result["email"],
                "message": result.get("message", "Login successful."),
            }
        return result

    @router.post("/logout")
    def logout(
        payload: UserLogoutRequest = Body(...),
        service: IUserService = Depends(get_service),
    ):
        return service.logout_user(payload.email)

    @router.post("/register")
    def register(
            payload: UserCredentialsRequest = Body(...),
            service: IUserService = Depends(get_service),
    ):
        result = service.register_user(payload.email, payload.password, payload.name)

        if result.get("status") == "success":
            token = create_access_token(payload.email)
            return {
                "status": "success",
                "access_token": token,
                "token_type": "bearer",
                "email": payload.email,
                "message": result.get("message", "Registration successful."),
            }

        return result

    @router.post("/test-result")
    def save_test_result(
        payload: UserQuizResultRequest = Body(...),
        service: IUserService = Depends(get_service),
    ):
        return service.save_test_result(
            payload.session_id,
            payload.answers,
            payload.profile,
            payload.roadmap,
            payload.email,
        )

    @router.get("/me")
    def get_me(current_user: str = Depends(get_current_user)):
        return {"email": current_user, "authenticated": True}

    @router.get("/profile")
    def get_profile(
        current_user: str = Depends(get_current_user),
        service: IUserService = Depends(get_service),
    ):
        return service.get_user_profile(current_user)

    @router.put("/profile")
    def update_profile(
        payload: UserProfileUpdateRequest = Body(...),
        current_user: str = Depends(get_current_user),
        service: IUserService = Depends(get_service),
    ):
        return service.update_user_profile(
            current_user,
            payload.new_email,
            payload.new_password,
        )

    return router
