from datetime import datetime, timezone
from typing import Any

from bson import ObjectId
from bson.errors import InvalidId

from backend.repositories.challenge_repository import PostRepository
from backend.repositories.challenge_submission_repository import ChallengeSubmissionRepository
from backend.business_logic.services.interfaces import IChallengeService


class ChallengeService(IChallengeService):
    def __init__(
        self,
        challenge_repository: PostRepository,
        submission_repository: ChallengeSubmissionRepository | None = None,
    ):
        self.challenge_repository = challenge_repository
        self.submission_repository = submission_repository or ChallengeSubmissionRepository()

    def get_challenges(self):
        try:
            challenges = list(self.challenge_repository.collection.find())
            for challenge in challenges:
                challenge["_id"] = str(challenge["_id"])
            return challenges
        except Exception as e:
            print(f"Error fetching challenges: {e}")
            return []

    def create_challenge(self, title: str):
        try:
            result = self.challenge_repository.create({"title": title})
            return {"message": "Challenge created", "id": str(result.inserted_id)}
        except Exception as e:
            return {"error": f"Failed to create challenge: {str(e)}"}

    def update_challenge(self, challenge_id: str, updates: dict) -> dict[str, Any]:
        try:
            oid = ObjectId(challenge_id)
        except InvalidId:
            return {"status": "error", "message": "Invalid challenge ID."}
        try:
            allowed = {"title", "description", "start_date", "end_date",
                       "registration_deadline", "tasks", "is_active"}
            safe = {k: v for k, v in updates.items() if k in allowed}
            if not safe:
                return {"status": "error", "message": "No valid fields to update."}
            result = self.challenge_repository.collection.update_one(
                {"_id": oid}, {"$set": safe}
            )
            if result.matched_count == 0:
                return {"status": "error", "message": "Challenge not found."}
            return {"status": "success", "message": "Challenge updated."}
        except Exception as e:
            return {"status": "error", "message": f"Update failed: {str(e)}"}

    def delete_challenge(self, challenge_id: str) -> dict[str, Any]:
        try:
            oid = ObjectId(challenge_id)
        except InvalidId:
            return {"status": "error", "message": "Invalid challenge ID."}
        try:
            result = self.challenge_repository.collection.delete_one({"_id": oid})
            if result.deleted_count == 0:
                return {"status": "error", "message": "Challenge not found."}
            return {"status": "success", "message": "Challenge deleted."}
        except Exception as e:
            return {"status": "error", "message": f"Delete failed: {str(e)}"}

    def register_for_challenge(self, challenge_id: str, user_email: str) -> dict[str, Any]:
        try:
            oid = ObjectId(challenge_id)
        except InvalidId:
            return {"status": "error", "message": "Invalid challenge ID."}
        try:
            result = self.challenge_repository.collection.update_one(
                {"_id": oid},
                {"$addToSet": {"participants": user_email}},
            )
            if result.matched_count == 0:
                return {"status": "error", "message": "Challenge not found."}
            return {"status": "success", "message": "Registered for challenge."}
        except Exception as e:
            return {"status": "error", "message": f"Registration failed: {str(e)}"}

    def get_leaderboard(self, challenge_id: str) -> dict[str, Any]:
        try:
            submissions = self.submission_repository.find_by_challenge(challenge_id)
            stats: dict[str, dict] = {}
            for sub in submissions:
                email = sub["user_email"]
                if email not in stats:
                    stats[email] = {"email": email, "completed_days": 0, "streak": 0}
                if sub.get("status") == "approved":
                    stats[email]["completed_days"] += 1

            leaderboard = sorted(
                stats.values(), key=lambda x: x["completed_days"], reverse=True
            )
            for rank, entry in enumerate(leaderboard, 1):
                entry["rank"] = rank
            return {"status": "success", "data": leaderboard}
        except Exception as e:
            return {"status": "error", "message": f"Failed to get leaderboard: {str(e)}"}

    def submit_proof(
        self, challenge_id: str, user_email: str, day: int, proof_url: str
    ) -> dict[str, Any]:
        try:
            now = datetime.now(timezone.utc).isoformat()
            data = {
                "challenge_id": challenge_id,
                "user_email": user_email,
                "day": day,
                "proof_url": proof_url,
                "status": "pending",
                "submitted_at": now,
            }
            sub_id = self.submission_repository.insert(data)
            return {
                "status": "success",
                "message": "Proof submitted. Awaiting review.",
                "submission_id": sub_id,
            }
        except Exception as e:
            return {"status": "error", "message": f"Submission failed: {str(e)}"}

    def get_submissions(self, challenge_id: str) -> dict[str, Any]:
        try:
            subs = self.submission_repository.find_by_challenge(challenge_id)
            return {"status": "success", "data": subs}
        except Exception as e:
            return {"status": "error", "message": f"Failed to get submissions: {str(e)}"}

    def moderate_submission(self, submission_id: str, status: str) -> dict[str, Any]:
        try:
            if status not in ("approved", "rejected"):
                return {"status": "error", "message": "status must be 'approved' or 'rejected'"}
            result = self.submission_repository.update_status(submission_id, status)
            if result is None or result.matched_count == 0:
                return {"status": "error", "message": "Submission not found."}
            return {"status": "success", "message": f"Submission {status}."}
        except Exception as e:
            return {"status": "error", "message": f"Moderation failed: {str(e)}"}
