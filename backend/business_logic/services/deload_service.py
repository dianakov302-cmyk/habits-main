from datetime import date, datetime, timezone
from typing import Any

from backend.repositories.deload_repository import DeloadRepository
from backend.business_logic.services.interfaces import IDeloadService

VALID_ACTIVITIES = {"meditation", "walk", "bath", "social_time", "digital_detox"}

ACTIVITY_LABELS = {
    "meditation": "Meditation",
    "walk": "Walk in Nature",
    "bath": "Relaxing Bath",
    "social_time": "Quality Social Time",
    "digital_detox": "Digital Detox",
}


class DeloadService(IDeloadService):
    def __init__(self, deload_repository: DeloadRepository):
        self.deload_repository = deload_repository

    def create_deload_day(self, email: str, trigger_streak: int) -> dict[str, Any]:
        """Called by streak/protocol logic when streak hits a multiple of 7."""
        try:
            today = date.today().isoformat()
            existing = self.deload_repository.find_by_email_and_date(email, today)
            if existing:
                return {"status": "success", "data": existing}

            data = {
                "trigger_streak": trigger_streak,
                "activity_chosen": None,
                "completed": False,
                "completed_at": None,
                "points_earned": 0,
            }
            self.deload_repository.upsert(email, today, data)
            doc = self.deload_repository.find_by_email_and_date(email, today)
            return {"status": "success", "data": doc}
        except Exception as e:
            return {"status": "error", "message": f"Failed to create deload day: {str(e)}"}

    def get_status(self, email: str) -> dict[str, Any]:
        try:
            active = self.deload_repository.find_active(email)
            if active is None:
                return {"status": "success", "data": {"active": False}}
            return {
                "status": "success",
                "data": {
                    "active": True,
                    "deload": active,
                    "activity_options": [
                        {"code": k, "label": v} for k, v in ACTIVITY_LABELS.items()
                    ],
                },
            }
        except Exception as e:
            return {"status": "error", "message": f"Failed to get deload status: {str(e)}"}

    def complete_deload(self, email: str, activity: str) -> dict[str, Any]:
        try:
            if activity not in VALID_ACTIVITIES:
                return {
                    "status": "error",
                    "message": f"Invalid activity. Choose from: {', '.join(VALID_ACTIVITIES)}",
                }
            active = self.deload_repository.find_active(email)
            if active is None:
                return {"status": "error", "message": "No active deload day found."}

            now = datetime.now(timezone.utc).isoformat()
            updates = {
                "activity_chosen": activity,
                "completed": True,
                "completed_at": now,
                "points_earned": 1,
            }
            self.deload_repository.upsert(email, active["date"], updates)
            return {
                "status": "success",
                "message": f"Deload day complete. +1 point. Streak preserved.",
                "activity": ACTIVITY_LABELS[activity],
            }
        except Exception as e:
            return {"status": "error", "message": f"Failed to complete deload: {str(e)}"}

    def get_history(self, email: str) -> dict[str, Any]:
        try:
            history = self.deload_repository.find_history(email)
            return {"status": "success", "data": history}
        except Exception as e:
            return {"status": "error", "message": f"Failed to fetch deload history: {str(e)}"}
