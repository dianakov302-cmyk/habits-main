from datetime import datetime, timezone, timedelta
from typing import Any

from backend.repositories.identity_repository import IdentityRepository
from backend.business_logic.services.interfaces import IIdentityService

LEVELS = [
    (90, "Elite"),
    (75, "Focused"),
    (60, "Disciplined"),
    (40, "Builder"),
    (20, "Explorer"),
    (0,  "Lost"),
]

LEVEL_ORDER = ["Lost", "Explorer", "Builder", "Disciplined", "Focused", "Elite"]


def _resolve_level(score: float) -> tuple[str, str, float]:
    """Return (current_level, next_level, progress_to_next_pct)."""
    level = "Lost"
    for threshold, name in LEVELS:
        if score >= threshold:
            level = name
            break

    idx = LEVEL_ORDER.index(level)
    next_level = LEVEL_ORDER[idx + 1] if idx < len(LEVEL_ORDER) - 1 else "Elite"

    if level == "Elite":
        progress_to_next = 100.0
    else:
        current_threshold = LEVELS[len(LEVELS) - 1 - idx][0]
        next_threshold = LEVELS[len(LEVELS) - 2 - idx][0] if idx < len(LEVEL_ORDER) - 1 else 100
        band = next_threshold - current_threshold
        progress_to_next = round(((score - current_threshold) / band) * 100, 1) if band > 0 else 100.0

    return level, next_level, progress_to_next


class IdentityService(IIdentityService):
    def __init__(self, identity_repository: IdentityRepository):
        self.identity_repository = identity_repository

    def get_profile(self, email: str) -> dict[str, Any]:
        try:
            doc = self.identity_repository.find_by_email(email)
            if doc is None:
                return self.recalculate(email)
            return {"status": "success", "data": doc}
        except Exception as e:
            return {"status": "error", "message": f"Failed to fetch identity: {str(e)}"}

    def recalculate(self, email: str) -> dict[str, Any]:
        """
        Recalculates identity score from existing data sources.
        Called by other services after significant events.
        For a full calculation, pass pre-computed metrics via the
        recalculate_with_metrics helper.
        """
        try:
            existing = self.identity_repository.find_by_email(email) or {}
            streak = existing.get("streak_score", 0.0)
            habit = existing.get("habit_completion_score", 0.0)
            protocol = existing.get("protocol_score", 0.0)
            reviews = existing.get("weekly_review_score", 0.0)
            program = existing.get("program_score", 0.0)

            score = round(
                streak * 0.30
                + habit * 0.30
                + protocol * 0.20
                + reviews * 0.10
                + program * 0.10,
                2,
            )
            level, next_level, progress = _resolve_level(score)

            data = {
                "identity_score": score,
                "identity_level": level,
                "next_level": next_level,
                "progress_to_next": progress,
                "streak_score": streak,
                "habit_completion_score": habit,
                "protocol_score": protocol,
                "weekly_review_score": reviews,
                "program_score": program,
            }
            self.identity_repository.upsert(email, data)
            return {"status": "success", "data": data}
        except Exception as e:
            return {"status": "error", "message": f"Recalculation failed: {str(e)}"}

    def update_component(self, email: str, component: str, value: float) -> None:
        """Update a single score component and trigger full recalculation."""
        existing = self.identity_repository.find_by_email(email) or {}
        existing[component] = round(min(max(value, 0.0), 100.0), 2)
        self.identity_repository.upsert(email, existing)
        self.recalculate(email)
