from backend.repositories.database import get_collection


class ProgramRepository:
    def __init__(self):
        self.collection = get_collection("user_programs")

    def find_active(self, email: str):
        return self.collection.find_one(
            {"email": email, "status": "active"}, {"_id": 0}
        )

    def find_by_email(self, email: str):
        cursor = self.collection.find({"email": email}, {"_id": 0}).sort(
            "created_at", -1
        )
        return list(cursor)

    def upsert_active(self, email: str, data: dict):
        data["email"] = email
        return self.collection.update_one(
            {"email": email, "status": "active"},
            {"$set": data},
            upsert=True,
        )

    def insert(self, data: dict):
        return self.collection.insert_one(data)
