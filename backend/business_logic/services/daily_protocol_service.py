from datetime import date
from typing import Any

from backend.repositories.daily_protocol_repository import DailyProtocolRepository
from backend.business_logic.services.interfaces import IDailyProtocolService

TASK_TYPES = {"minimum", "target", "bonus"}
TASK_POINTS = {"minimum": 1, "target": 2, "bonus": 3}


class DailyProtocolService(IDailyProtocolService):
    def __init__(self, daily_protocol_repository: DailyProtocolRepository):
        self.daily_protocol_repository = daily_protocol_repository

    def get_today(self, email: str) -> dict[str, Any]:
        try:
            today = date.today().isoformat()
            doc = self.daily_protocol_repository.find_by_email_and_date(email, today)
            if doc is None:
                return {
                    "status": "success",
                    "data": None,
                    "message": "No protocol for today. Create one via POST /protocol/create",
                }
            return {"status": "success", "data": doc}
        except Exception as e:
            return {"status": "error", "message": f"Failed to get today's protocol: {str(e)}"}

    def create_protocol(
        self,
        email: str,
        date_str: str,
        minimum_task: str,
        target_task: str,
        bonus_task: str,
    ) -> dict[str, Any]:
        try:
            existing = self.daily_protocol_repository.find_by_email_and_date(email, date_str)
            if existing:
                return {"status": "error", "message": "Protocol already exists for this date."}

            data = {
                "minimum_task": {"title": minimum_task, "completed": False},
                "target_task": {"title": target_task, "completed": False},
                "bonus_task": {"title": bonus_task, "completed": False},
                "points_earned": 0,
                "streak_counts": False,
            }
            self.daily_protocol_repository.upsert(email, date_str, data)
            doc = self.daily_protocol_repository.find_by_email_and_date(email, date_str)
            return {"status": "success", "data": doc}
        except Exception as e:
            return {"status": "error", "message": f"Failed to create protocol: {str(e)}"}

    def complete_task(self, email: str, date_str: str, task_type: str) -> dict[str, Any]:
        try:
            if task_type not in TASK_TYPES:
                return {
                    "status": "error",
                    "message": f"task_type must be one of: {', '.join(TASK_TYPES)}",
                }

            doc = self.daily_protocol_repository.find_by_email_and_date(email, date_str)
            if doc is None:
                return {"status": "error", "message": "Protocol not found for this date."}

            task_key = f"{task_type}_task"
            if doc.get(task_key, {}).get("completed"):
                return {"status": "success", "message": "Task already completed.", "data": doc}

            updates = {
                f"{task_key}.completed": True,
            }

            # Recalculate points — sum of completed task points
            points = 0
            for t in TASK_TYPES:
                key = f"{t}_task"
                already_done = doc.get(key, {}).get("completed", False)
                if t == task_type or already_done:
                    points += TASK_POINTS[t]

            updates["points_earned"] = points

            # Streak counts when minimum is done
            minimum_done = (
                doc.get("minimum_task", {}).get("completed", False)
                or task_type == "minimum"
            )
            updates["streak_counts"] = minimum_done

            self.daily_protocol_repository.upsert(email, date_str, updates)
            updated = self.daily_protocol_repository.find_by_email_and_date(email, date_str)
            return {
                "status": "success",
                "message": f"{task_type.capitalize()} task completed. +{TASK_POINTS[task_type]} point(s).",
                "data": updated,
            }
        except Exception as e:
            return {"status": "error", "message": f"Failed to complete task: {str(e)}"}

    def get_history(self, email: str, days: int = 30) -> dict[str, Any]:
        try:
            history = self.daily_protocol_repository.find_recent(email, limit=days)
            return {"status": "success", "data": history}
        except Exception as e:
            return {"status": "error", "message": f"Failed to fetch history: {str(e)}"}
