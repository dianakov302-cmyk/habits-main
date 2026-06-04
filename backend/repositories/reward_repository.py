from backend.repositories.database import get_collection


class RewardRepository:
    def __init__(self):
        self.collection = get_collection("user_rewards")

    def find_by_email(self, email: str):
        return self.collection.find_one({"email": email}, {"_id": 0})

    def upsert(self, email: str, data: dict):
        data["email"] = email
        return self.collection.update_one(
            {"email": email},
            {"$set": data},
            upsert=True,
        )

    def add_unlocked(self, email: str, reward_code: str, unlocked_at: str):
        return self.collection.update_one(
            {"email": email},
            {
                "$addToSet": {"unlocked": reward_code},
                "$set": {f"unlocked_at.{reward_code}": unlocked_at},
            },
            upsert=True,
        )
