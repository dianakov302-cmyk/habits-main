from pydantic import BaseModel, Field
from typing import Any


# ── Users ──────────────────────────────────────────────────────────────────

class UserCredentialsRequest(BaseModel):
    email: str = Field(..., min_length=3, max_length=320)
    password: str = Field(..., min_length=1)
    name: str | None = Field(default=None, min_length=1, max_length=200)


class UserLogoutRequest(BaseModel):
    email: str = Field(..., min_length=3, max_length=320)


class UserProfileUpdateRequest(BaseModel):
    email: str | None = Field(default=None, min_length=3, max_length=320)
    new_email: str | None = Field(default=None, min_length=3, max_length=320)
    new_password: str | None = Field(default=None, min_length=1)


class UserQuizResultRequest(BaseModel):
    session_id: str = Field(..., min_length=8)
    email: str | None = Field(default=None, min_length=3, max_length=320)
    answers: list[str] = Field(default_factory=list)
    profile: dict[str, Any] = Field(default_factory=dict)
    roadmap: dict[str, Any] = Field(default_factory=dict)


class HabitCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1, max_length=1000)


class GroupCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)


class GroupJoinRequest(BaseModel):
    group_id: str = Field(..., min_length=1)
    user_id: str = Field(..., min_length=1)


class ChallengeCreateRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)


class HabitCompletionRequest(BaseModel):
    user_id: str = Field(..., min_length=1)
    habit_id: str = Field(..., min_length=1)


class GoalCreateRequest(BaseModel):
    email: str | None = Field(default=None, min_length=3, max_length=320)
    goal_code: str = Field(..., min_length=1, max_length=100)


# ── Identity ────────────────────────────────────────────────────────────────

class IdentityRecalculateRequest(BaseModel):
    email: str = Field(..., min_length=3, max_length=320)


# ── Daily Protocol ──────────────────────────────────────────────────────────

class DailyProtocolCreateRequest(BaseModel):
    email: str = Field(..., min_length=3, max_length=320)
    date: str = Field(..., description="YYYY-MM-DD", min_length=10, max_length=10)
    minimum_task: str = Field(..., min_length=1, max_length=300)
    target_task: str = Field(..., min_length=1, max_length=300)
    bonus_task: str = Field(..., min_length=1, max_length=300)


class DailyProtocolCompleteRequest(BaseModel):
    email: str = Field(..., min_length=3, max_length=320)
    date: str = Field(..., description="YYYY-MM-DD", min_length=10, max_length=10)
    task_type: str = Field(..., description="minimum | target | bonus")


# ── Deload ──────────────────────────────────────────────────────────────────

class DeloadCompleteRequest(BaseModel):
    email: str = Field(..., min_length=3, max_length=320)
    activity: str = Field(
        ...,
        description="meditation | walk | bath | social_time | digital_detox",
    )


# ── 30-Day Program ──────────────────────────────────────────────────────────

class ProgramStartRequest(BaseModel):
    email: str = Field(..., min_length=3, max_length=320)
    goal_code: str = Field(..., min_length=1, max_length=100)
    level: str = Field(
        default="beginner",
        description="beginner | medium | advanced",
    )


class ProgramCompleteDayRequest(BaseModel):
    email: str = Field(..., min_length=3, max_length=320)


# ── Weekly Review ───────────────────────────────────────────────────────────

class WeeklyReviewSubmitRequest(BaseModel):
    email: str = Field(..., min_length=3, max_length=320)
    what_worked: str = Field(..., min_length=1, max_length=2000)
    what_distracted: str = Field(..., min_length=1, max_length=2000)
    what_to_change: str = Field(..., min_length=1, max_length=2000)


# ── Rewards ─────────────────────────────────────────────────────────────────

class RewardCheckRequest(BaseModel):
    email: str = Field(..., min_length=3, max_length=320)
    current_streak: int = Field(default=0, ge=0)
    completed_programs: int = Field(default=0, ge=0)
    weekly_reviews: int = Field(default=0, ge=0)


class RewardActivateRequest(BaseModel):
    email: str = Field(..., min_length=3, max_length=320)
    reward_code: str = Field(..., min_length=1, max_length=100)


# ── Challenge Extensions ────────────────────────────────────────────────────

class ChallengeUpdateRequest(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    start_date: str | None = Field(default=None)
    end_date: str | None = Field(default=None)
    registration_deadline: str | None = Field(default=None)
    is_active: bool | None = Field(default=None)


class ChallengeRegisterRequest(BaseModel):
    user_email: str = Field(..., min_length=3, max_length=320)


class ChallengeSubmitProofRequest(BaseModel):
    user_email: str = Field(..., min_length=3, max_length=320)
    day: int = Field(..., ge=1, le=30)
    proof_url: str = Field(..., min_length=1, max_length=2000)


class ChallengeModerateRequest(BaseModel):
    status: str = Field(..., description="approved | rejected")


# ── Chat ────────────────────────────────────────────────────────────────────

class ChatStartDMRequest(BaseModel):
    sender_email: str = Field(..., min_length=3, max_length=320)
    recipient_email: str = Field(..., min_length=3, max_length=320)


class ChatSendMessageRequest(BaseModel):
    sender_email: str = Field(..., min_length=3, max_length=320)
    content: str = Field(..., min_length=1, max_length=4000)


# ── Productivity — Water ────────────────────────────────────────────────────

class WaterLogRequest(BaseModel):
    email: str = Field(..., min_length=3, max_length=320)
    date: str = Field(..., description="YYYY-MM-DD", min_length=10, max_length=10)
    amount_ml: int = Field(default=250, ge=50, le=2000)


class WaterGoalRequest(BaseModel):
    email: str = Field(..., min_length=3, max_length=320)
    goal_glasses: int = Field(..., ge=1, le=20)


# ── Productivity — Planner ──────────────────────────────────────────────────

class PlannerTaskCreateRequest(BaseModel):
    email: str = Field(..., min_length=3, max_length=320)
    date: str = Field(..., description="YYYY-MM-DD", min_length=10, max_length=10)
    title: str = Field(..., min_length=1, max_length=300)
    description: str = Field(default="", max_length=2000)
    priority: str = Field(default="medium", description="high | medium | low")
    time_slot: str = Field(default="", max_length=50)


class PlannerTaskUpdateRequest(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=300)
    description: str | None = Field(default=None, max_length=2000)
    priority: str | None = Field(default=None, description="high | medium | low")
    time_slot: str | None = Field(default=None, max_length=50)


# ── Productivity — Spaced Repetition ────────────────────────────────────────

class SRCardCreateRequest(BaseModel):
    email: str = Field(..., min_length=3, max_length=320)
    deck: str = Field(..., min_length=1, max_length=100)
    front: str = Field(..., min_length=1, max_length=1000)
    back: str = Field(..., min_length=1, max_length=1000)


class SRCardReviewRequest(BaseModel):
    ease: int = Field(..., ge=1, le=4, description="1=again 2=hard 3=good 4=easy")


# ── Productivity — Brainstorm ────────────────────────────────────────────────

class BrainstormCreateRequest(BaseModel):
    email: str = Field(..., min_length=3, max_length=320)
    title: str = Field(..., min_length=1, max_length=200)
    tags: list[str] = Field(default_factory=list)


class BrainstormIdeaRequest(BaseModel):
    content: str = Field(..., min_length=1, max_length=2000)
