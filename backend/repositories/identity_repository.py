from datetime import datetime, timezone

from backend.repositories.database import get_collection


class IdentityRepository:
    def __init__(self):
        self.collection = get_collection("user_identity")

    def find_by_email(self, email: str):
        return self.collection.find_one({"email": email}, {"_id": 0})

    def upsert(self, email: str, data: dict):
        data["email"] = email
        data["last_calculated_at"] = datetime.now(timezone.utc).isoformat()
        return self.collection.update_one(
            {"email": email},
            {"$set": data},
            upsert=True,
        )
