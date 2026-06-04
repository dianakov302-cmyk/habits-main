from backend.repositories.database import get_collection


class WeeklyReviewRepository:
    def __init__(self):
        self.collection = get_collection("weekly_reviews")

    def insert(self, data: dict):
        return self.collection.insert_one(data)

    def find_latest(self, email: str):
        return self.collection.find_one(
            {"email": email}, {"_id": 0}, sort=[("created_at", -1)]
        )

    def find_history(self, email: str):
        cursor = self.collection.find({"email": email}, {"_id": 0}).sort(
            "created_at", -1
        )
        return list(cursor)

    def count_recent(self, email: str, since_iso: str) -> int:
        return self.collection.count_documents(
            {"email": email, "created_at": {"$gte": since_iso}}
        )
