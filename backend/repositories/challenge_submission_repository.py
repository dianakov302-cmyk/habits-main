from bson import ObjectId
from bson.errors import InvalidId

from backend.repositories.database import get_collection


class ChallengeSubmissionRepository:
    def __init__(self):
        self.submissions = get_collection("challenge_submissions")

    def insert(self, data: dict) -> str:
        result = self.submissions.insert_one(data)
        return str(result.inserted_id)

    def find_by_challenge(self, challenge_id: str):
        cursor = self.submissions.find({"challenge_id": challenge_id}, {"_id": 1,
                                        "challenge_id": 1, "user_email": 1,
                                        "day": 1, "proof_url": 1, "status": 1,
                                        "submitted_at": 1})
        docs = list(cursor)
        for d in docs:
            d["_id"] = str(d["_id"])
        return docs

    def find_by_user_and_challenge(self, user_email: str, challenge_id: str):
        cursor = self.submissions.find(
            {"user_email": user_email, "challenge_id": challenge_id},
            {"_id": 1, "day": 1, "proof_url": 1, "status": 1, "submitted_at": 1},
        )
        docs = list(cursor)
        for d in docs:
            d["_id"] = str(d["_id"])
        return docs

    def update_status(self, submission_id: str, status: str):
        try:
            oid = ObjectId(submission_id)
        except InvalidId:
            return None
        return self.submissions.update_one(
            {"_id": oid}, {"$set": {"status": status}}
        )
