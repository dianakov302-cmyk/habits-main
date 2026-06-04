from backend.repositories.database import get_collection


class GoalRepository:
    def __init__(self):
        self.collection = get_collection("goals")

    def find_by_email(self, email: str):
        return self.collection.find_one({"email": email})

    def upsert_goal(self, email: str, data: dict):
        return self.collection.update_one(
            {"email": email},
            {"$set": data},
            upsert=True,
        )
