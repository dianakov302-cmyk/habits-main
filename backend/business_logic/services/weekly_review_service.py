from datetime import datetime, timezone
from typing import Any

from backend.repositories.weekly_review_repository import WeeklyReviewRepository
from backend.business_logic.services.interfaces import IWeeklyReviewService


def _generate_suggestions(what_worked: str, what_distracted: str, what_to_change: str) -> list[str]:
    suggestions = []
    text = (what_distracted + " " + what_to_change).lower()

    if "phone" in text or "social media" in text or "scroll" in text:
        suggestions.append("Try a 1-hour digital sunset before bed — no phone, just wind-down.")
    if "focus" in text or "distract" in text or "concentrat" in text:
        suggestions.append("Protect your first 90 minutes in the morning as sacred deep-work time.")
    if "sleep" in text or "tired" in text or "energy" in text:
        suggestions.append("Anchor your sleep schedule — same bedtime and wake time every day.")
    if "plan" in text or "organize" in text or "schedule" in text:
        suggestions.append("Use the daily planner to time-block your top 3 priorities each morning.")
    if "exercise" in text or "workout" in text or "movement" in text:
        suggestions.append("Commit to movement before checking any messages — even a 15-min walk counts.")
    if not suggestions:
        suggestions.append("Consistency over intensity. One small improvement each week compounds.")
        suggestions.append("Review your minimum task — if it feels easy, that's the point. Keep it.")

    return suggestions


def _generate_reflection(what_worked: str, what_to_change: str) -> str:
    return (
        f"This week, your consistency showed in what worked: {what_worked}. "
        f"Next week, focusing on '{what_to_change}' will compound your progress. "
        "Small, deliberate shifts are the engine of lasting change."
    )


class WeeklyReviewService(IWeeklyReviewService):
    def __init__(self, weekly_review_repository: WeeklyReviewRepository):
        self.weekly_review_repository = weekly_review_repository

    def submit_review(
        self,
        email: str,
        what_worked: str,
        what_distracted: str,
        what_to_change: str,
    ) -> dict[str, Any]:
        try:
            now = datetime.now(timezone.utc)
            week_number = now.isocalendar()[1]

            suggestions = _generate_suggestions(what_worked, what_distracted, what_to_change)
            reflection = _generate_reflection(what_worked, what_to_change)

            doc = {
                "email": email,
                "week_number": week_number,
                "year": now.year,
                "what_worked": what_worked,
                "what_distracted": what_distracted,
                "what_to_change": what_to_change,
                "suggestions": suggestions,
                "reflection": reflection,
                "created_at": now.isoformat(),
            }
            self.weekly_review_repository.insert(doc)
            doc.pop("_id", None)
            return {
                "status": "success",
                "message": "Review saved.",
                "data": {
                    "suggestions": suggestions,
                    "reflection": reflection,
                    "week_number": week_number,
                },
            }
        except Exception as e:
            return {"status": "error", "message": f"Failed to save review: {str(e)}"}

    def get_history(self, email: str) -> dict[str, Any]:
        try:
            history = self.weekly_review_repository.find_history(email)
            return {"status": "success", "data": history}
        except Exception as e:
            return {"status": "error", "message": f"Failed to fetch review history: {str(e)}"}

    def get_latest(self, email: str) -> dict[str, Any]:
        try:
            doc = self.weekly_review_repository.find_latest(email)
            if doc is None:
                return {"status": "error", "message": "No reviews found."}
            return {"status": "success", "data": doc}
        except Exception as e:
            return {"status": "error", "message": f"Failed to fetch latest review: {str(e)}"}
