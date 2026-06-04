import sys
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# existing services
from backend.business_logic.services.challenge_service import ChallengeService
from backend.business_logic.services.goal_service import GoalService
from backend.business_logic.services.groups_service import GroupService
from backend.business_logic.services.habit_service import HabitService
from backend.business_logic.services.progress_service import ProgressService
from backend.business_logic.services.user_service import UserService
# new services
from backend.business_logic.services.identity_service import IdentityService
from backend.business_logic.services.daily_protocol_service import DailyProtocolService
from backend.business_logic.services.deload_service import DeloadService
from backend.business_logic.services.program_service import ProgramService
from backend.business_logic.services.weekly_review_service import WeeklyReviewService
from backend.business_logic.services.reward_service import RewardService
from backend.business_logic.services.chat_service import ChatService
from backend.business_logic.services.productivity_service import ProductivityService

# existing controllers
from backend.controllers.challenges_controller import (
    create_router as create_challenges_router,
)
from backend.controllers.goal_controller import create_router as create_goal_router
from backend.controllers.groups_controller import create_router as create_groups_router
from backend.controllers.habit_controller import create_router as create_habit_router
from backend.controllers.progress_controller import create_router as create_progress_router
from backend.controllers.user_controller import create_router as create_user_router
# new controllers
from backend.controllers.identity_controller import create_router as create_identity_router
from backend.controllers.daily_protocol_controller import create_router as create_protocol_router
from backend.controllers.deload_controller import create_router as create_deload_router
from backend.controllers.program_controller import create_router as create_program_router
from backend.controllers.weekly_review_controller import create_router as create_reviews_router
from backend.controllers.reward_controller import create_router as create_rewards_router
from backend.controllers.chat_controller import create_router as create_chat_router
from backend.controllers.productivity_controller import create_router as create_productivity_router

# existing repositories
from backend.repositories.challenge_repository import PostRepository
from backend.repositories.database import ping_database
from backend.repositories.goal_repository import GoalRepository
from backend.repositories.groups_repository import GroupRepository
from backend.repositories.habit_repository import HabitRepository
from backend.repositories.progress_repository import ProgressRepository
from backend.repositories.user_repository import UserRepository
# new repositories
from backend.repositories.identity_repository import IdentityRepository
from backend.repositories.daily_protocol_repository import DailyProtocolRepository
from backend.repositories.deload_repository import DeloadRepository
from backend.repositories.program_repository import ProgramRepository
from backend.repositories.weekly_review_repository import WeeklyReviewRepository
from backend.repositories.reward_repository import RewardRepository
from backend.repositories.chat_repository import ChatRepository
from backend.repositories.productivity_repository import ProductivityRepository
from backend.repositories.challenge_submission_repository import ChallengeSubmissionRepository

load_dotenv()

STATIC_DIR = Path(__file__).resolve().parents[1] / "frontend" / "site"


class Container:
    def __init__(self):
        # existing repositories
        self._user_repository = None
        self._habit_repository = None
        self._group_repository = None
        self._challenge_repository = None
        self._progress_repository = None
        self._goal_repository = None
        # new repositories
        self._identity_repository = None
        self._daily_protocol_repository = None
        self._deload_repository = None
        self._program_repository = None
        self._weekly_review_repository = None
        self._reward_repository = None
        self._chat_repository = None
        self._productivity_repository = None
        self._challenge_submission_repository = None

        # existing services
        self._user_service = None
        self._habit_service = None
        self._group_service = None
        self._challenge_service = None
        self._progress_service = None
        self._goal_service = None
        # new services
        self._identity_service = None
        self._daily_protocol_service = None
        self._deload_service = None
        self._program_service = None
        self._weekly_review_service = None
        self._reward_service = None
        self._chat_service = None
        self._productivity_service = None

    # ── existing services ──────────────────────────────────────────────────

    def get_user_service(self):
        if self._user_service is None:
            self._user_repository = self._user_repository or UserRepository()
            self._user_service = UserService(self._user_repository)
        return self._user_service

    def get_habit_service(self):
        if self._habit_service is None:
            self._habit_repository = self._habit_repository or HabitRepository()
            self._habit_service = HabitService(self._habit_repository)
        return self._habit_service

    def get_group_service(self):
        if self._group_service is None:
            self._group_repository = self._group_repository or GroupRepository()
            self._group_service = GroupService(self._group_repository)
        return self._group_service

    def get_challenge_service(self):
        if self._challenge_service is None:
            self._challenge_repository = self._challenge_repository or PostRepository()
            self._challenge_submission_repository = (
                self._challenge_submission_repository or ChallengeSubmissionRepository()
            )
            self._challenge_service = ChallengeService(
                self._challenge_repository, self._challenge_submission_repository
            )
        return self._challenge_service

    def get_progress_service(self):
        if self._progress_service is None:
            self._progress_repository = self._progress_repository or ProgressRepository()
            self._progress_service = ProgressService(self._progress_repository)
        return self._progress_service

    def get_goal_service(self):
        if self._goal_service is None:
            self._goal_repository = self._goal_repository or GoalRepository()
            self._goal_service = GoalService(self._goal_repository)
        return self._goal_service

    # ── new services ───────────────────────────────────────────────────────

    def get_identity_service(self):
        if self._identity_service is None:
            self._identity_repository = self._identity_repository or IdentityRepository()
            self._identity_service = IdentityService(self._identity_repository)
        return self._identity_service

    def get_daily_protocol_service(self):
        if self._daily_protocol_service is None:
            self._daily_protocol_repository = (
                self._daily_protocol_repository or DailyProtocolRepository()
            )
            self._daily_protocol_service = DailyProtocolService(self._daily_protocol_repository)
        return self._daily_protocol_service

    def get_deload_service(self):
        if self._deload_service is None:
            self._deload_repository = self._deload_repository or DeloadRepository()
            self._deload_service = DeloadService(self._deload_repository)
        return self._deload_service

    def get_program_service(self):
        if self._program_service is None:
            self._program_repository = self._program_repository or ProgramRepository()
            self._program_service = ProgramService(self._program_repository)
        return self._program_service

    def get_weekly_review_service(self):
        if self._weekly_review_service is None:
            self._weekly_review_repository = (
                self._weekly_review_repository or WeeklyReviewRepository()
            )
            self._weekly_review_service = WeeklyReviewService(self._weekly_review_repository)
        return self._weekly_review_service

    def get_reward_service(self):
        if self._reward_service is None:
            self._reward_repository = self._reward_repository or RewardRepository()
            self._reward_service = RewardService(self._reward_repository)
        return self._reward_service

    def get_chat_service(self):
        if self._chat_service is None:
            self._chat_repository = self._chat_repository or ChatRepository()
            self._user_repository = self._user_repository or UserRepository()
            self._chat_service = ChatService(self._chat_repository, self._user_repository)
        return self._chat_service

    def get_productivity_service(self):
        if self._productivity_service is None:
            self._productivity_repository = (
                self._productivity_repository or ProductivityRepository()
            )
            self._productivity_service = ProductivityService(self._productivity_repository)
        return self._productivity_service


def create_app() -> FastAPI:
    container = Container()

    app = FastAPI(
        title="backend API",
        version="1.0.0",
        description="API server for habits, progress tracking, groups, challenges, and users.",
    )

    app.state.container = container

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://127.0.0.1:3000",
            "http://localhost:3000",
            "http://127.0.0.1:8080",
            "http://localhost:8080",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # existing routers
    app.include_router(create_user_router(container.get_user_service))
    app.include_router(create_progress_router(container.get_progress_service))
    app.include_router(create_habit_router(container.get_habit_service))
    app.include_router(create_groups_router(container.get_group_service))
    app.include_router(create_challenges_router(container.get_challenge_service))
    app.include_router(create_goal_router(container.get_goal_service))
    # new routers
    app.include_router(create_identity_router(container.get_identity_service))
    app.include_router(create_protocol_router(container.get_daily_protocol_service))
    app.include_router(create_deload_router(container.get_deload_service))
    app.include_router(create_program_router(container.get_program_service))
    app.include_router(create_reviews_router(container.get_weekly_review_service))
    app.include_router(create_rewards_router(container.get_reward_service))
    app.include_router(create_chat_router(container.get_chat_service))
    app.include_router(create_productivity_router(container.get_productivity_service))
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

    import os as _os
    _img_dir = _os.path.join(_os.path.dirname(__file__), "..", "frontend", "img")
    if _os.path.exists(_img_dir):
        app.mount("/img", StaticFiles(directory=_img_dir), name="images")

    @app.get("/", summary="Root")
    def root():
        return {
            "message": "backend API is running",
            "docs": "/docs",
            "health": "/health",
            "ui": "/app",
        }

    @app.get("/app", summary="Web UI")
    def web_app():
        return FileResponse(STATIC_DIR / "index.html")

    @app.get("/health", summary="Health Check")
    def health():
        is_connected = ping_database()
        return {
            "status": "ok" if is_connected else "degraded",
            "database": "connected" if is_connected else "unavailable",
        }

    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8080, reload=True)
