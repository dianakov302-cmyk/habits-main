from backend.repositories.database import get_collection


class DailyProtocolRepository:
    def __init__(self):
        self.collection = get_collection("daily_protocols")

    def find_by_email_and_date(self, email: str, date: str):
        return self.collection.find_one({"email": email, "date": date}, {"_id": 0})

    def upsert(self, email: str, date: str, data: dict):
        data["email"] = email
        data["date"] = date
        return self.collection.update_one(
            {"email": email, "date": date},
            {"$set": data},
            upsert=True,
        )

    def find_recent(self, email: str, limit: int = 30):
        cursor = (
            self.collection.find({"email": email}, {"_id": 0})
            .sort("date", -1)
            .limit(limit)
        )
        return list(cursor)
