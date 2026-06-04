from backend.domain.models.schemas import PunchCard


class LoyaltyService:
    def __init__(self, repo: PunchCard):
        self.repo = repo

    async def add_punch_to_user(self, user_id: str):
        card = await self.repo.update_punch(user_id, "daily_habits")

        if card and card["punches_earned"] == card["total_needed"]:
            await self.repo.mark_as_completed(card["_id"])
            return {"status": "completed", "reward": "Unlocking Cosmos Theme!"}

        return {"status": "punched", "current": card["punches_earned"] if card else 1}
