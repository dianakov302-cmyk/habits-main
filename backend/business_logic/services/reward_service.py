from datetime import datetime, timezone
from typing import Any

from backend.repositories.reward_repository import RewardRepository
from backend.business_logic.services.interfaces import IRewardService

REWARD_CATALOG = [
    {
        "code": "avatar_frame_7",
        "title": "Silver Ring",
        "description": "A subtle silver avatar frame. Earned at 7-day streak.",
        "type": "avatar_frame",
        "trigger": "streak_7",
        "required_streak": 7,
    },
    {
        "code": "theme_midnight",
        "title": "Midnight Theme",
        "description": "Deep navy profile theme with subtle shimmer. Earned at 14-day streak.",
        "type": "profile_theme",
        "trigger": "streak_14",
        "required_streak": 14,
    },
    {
        "code": "bg_elite",
        "title": "Elite Background",
        "description": "Animated cosmic background. Earned at 30-day streak.",
        "type": "background",
        "trigger": "streak_30",
        "required_streak": 30,
    },
    {
        "code": "focus_room",
        "title": "Focus Room",
        "description": "Customizable focus environment. Earned at 60-day streak.",
        "type": "focus_room",
        "trigger": "streak_60",
        "required_streak": 60,
    },
    {
        "code": "program_complete",
        "title": "30-Day Completion",
        "description": "Marks the completion of a 30-day program.",
        "type": "badge",
        "trigger": "program_complete_1",
        "required_programs": 1,
    },
    {
        "code": "frame_reflection",
        "title": "Reflection Master",
        "description": "Avatar frame for completing 5 weekly reviews.",
        "type": "avatar_frame",
        "trigger": "reviews_5",
        "required_reviews": 5,
    },
]

_BY_CODE = {r["code"]: r for r in REWARD_CATALOG}


class RewardService(IRewardService):
    def __init__(self, reward_repository: RewardRepository):
        self.reward_repository = reward_repository

    def get_catalog(self) -> dict[str, Any]:
        return {"status": "success", "data": REWARD_CATALOG}

    def get_user_rewards(self, email: str) -> dict[str, Any]:
        try:
            doc = self.reward_repository.find_by_email(email)
            if doc is None:
                return {"status": "success", "data": {"unlocked": [], "active_theme": "default"}}
            return {"status": "success", "data": doc}
        except Exception as e:
            return {"status": "error", "message": f"Failed to fetch rewards: {str(e)}"}

    def check_and_unlock(
        self,
        email: str,
        current_streak: int = 0,
        completed_programs: int = 0,
        weekly_reviews: int = 0,
    ) -> dict[str, Any]:
        try:
            doc = self.reward_repository.find_by_email(email) or {}
            already_unlocked: set[str] = set(doc.get("unlocked", []))
            newly_unlocked = []
            now = datetime.now(timezone.utc).isoformat()

            for reward in REWARD_CATALOG:
                code = reward["code"]
                if code in already_unlocked:
                    continue
                earned = False
                if "required_streak" in reward and current_streak >= reward["required_streak"]:
                    earned = True
                elif "required_programs" in reward and completed_programs >= reward["required_programs"]:
                    earned = True
                elif "required_reviews" in reward and weekly_reviews >= reward["required_reviews"]:
                    earned = True

                if earned:
                    self.reward_repository.add_unlocked(email, code, now)
                    newly_unlocked.append({"code": code, "title": reward["title"]})

            return {
                "status": "success",
                "newly_unlocked": newly_unlocked,
                "message": (
                    f"Unlocked {len(newly_unlocked)} new reward(s)."
                    if newly_unlocked
                    else "No new rewards unlocked."
                ),
            }
        except Exception as e:
            return {"status": "error", "message": f"Failed to check rewards: {str(e)}"}

    def activate_reward(self, email: str, reward_code: str) -> dict[str, Any]:
        try:
            if reward_code not in _BY_CODE:
                return {"status": "error", "message": "Unknown reward code."}

            doc = self.reward_repository.find_by_email(email) or {}
            if reward_code not in doc.get("unlocked", []):
                return {"status": "error", "message": "Reward not unlocked yet."}

            reward = _BY_CODE[reward_code]
            field_map = {
                "avatar_frame": "active_avatar_frame",
                "profile_theme": "active_theme",
                "background": "active_background",
                "focus_room": "active_focus_room",
            }
            field = field_map.get(reward["type"])
            if not field:
                return {"status": "error", "message": "This reward type cannot be activated."}

            self.reward_repository.upsert(email, {field: reward_code})
            return {
                "status": "success",
                "message": f"{reward['title']} activated.",
                "activated": reward_code,
            }
        except Exception as e:
            return {"status": "error", "message": f"Failed to activate reward: {str(e)}"}
