from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from backend.repositories.database import get_collection


class UserRepository:
    def __init__(self):
        self.collection = get_collection("users")
        self.quiz_results_collection = get_collection("quiz_results")

    def create_user(self, user_data: dict[str, Any]):
        document = {
            "email": user_data["email"],
            "password": user_data["password"],
            "name": user_data.get("name", ""),
            "auth_provider": user_data.get("auth_provider", "email"),
            "verified": user_data.get("verified", False),
            "created_at": user_data.get("created_at")
            or datetime.now(timezone.utc).isoformat(),
        }

        for key, value in user_data.items():
            if key not in document:
                document[key] = value

        return self.collection.insert_one(document)

    def find_by_email(self, email: str):
        return self.collection.find_one({"email": email})

    def find_by_id(self, user_id):
        return self.collection.find_one({"_id": user_id})

    def update_by_email(self, email: str, update_fields: dict[str, Any]):
        return self.collection.update_one({"email": email}, {"$set": update_fields})

    def save_quiz_result(self, result_data: dict[str, Any]) -> dict[str, Any]:
        now = datetime.now(timezone.utc).isoformat()
        session_id = result_data["session_id"]
        email = result_data.get("email")
        payload = {
            "session_id": session_id,
            "email": email,
            "answers": result_data.get("answers", []),
            "profile": result_data.get("profile", {}),
            "roadmap": result_data.get("roadmap", {}),
            "saved_at": now,
        }

        if email:
            user = self.find_by_email(email)
            if user:
                self.update_by_email(
                    email,
                    {
                        "quiz_profile": payload["profile"],
                        "quiz_roadmap": payload["roadmap"],
                        "quiz_answers": payload["answers"],
                        "quiz_session_id": session_id,
                        "quiz_saved_at": now,
                    },
                )
                return {"storage": "users", "email": email, "saved_at": now}

        self.quiz_results_collection.update_one(
            {"session_id": session_id},
            {"$set": payload},
            upsert=True,
        )
        return {"storage": "quiz_results", "session_id": session_id, "saved_at": now}
