import unittest

from backend.business_logic.services.challenge_service import ChallengeService


class FakePostRepository:
    def __init__(self):
        self._store: dict[str, dict] = {}
        self._counter = 0
        self.collection = self

    def _next_id(self):
        from bson import ObjectId
        return ObjectId()

    def find(self, query=None):
        return list(self._store.values())

    def insert_one(self, data):
        from bson import ObjectId
        oid = ObjectId()
        data["_id"] = oid
        self._store[str(oid)] = data.copy()
        class R:
            inserted_id = oid
        return R()

    def create(self, data):
        return self.insert_one(data)

    def update_one(self, query, update, upsert=False):
        class R:
            matched_count = 0
        return R()

    def delete_one(self, query):
        class R:
            deleted_count = 0
        return R()


class FakeSubmissionRepository:
    def __init__(self):
        self._store: dict[str, dict] = {}
        self._counter = 0

    def insert(self, data):
        self._counter += 1
        sid = str(self._counter)
        self._store[sid] = {"_id": sid, **data}
        return sid

    def find_by_challenge(self, challenge_id):
        return [s for s in self._store.values() if s["challenge_id"] == challenge_id]

    def find_by_user_and_challenge(self, user_email, challenge_id):
        return [s for s in self._store.values()
                if s["user_email"] == user_email and s["challenge_id"] == challenge_id]

    def update_status(self, submission_id, status):
        if submission_id not in self._store:
            class R:
                matched_count = 0
            return R()
        self._store[submission_id]["status"] = status
        class R:
            matched_count = 1
        return R()


class ChallengeServiceTests(unittest.TestCase):
    def setUp(self):
        self.post_repo = FakePostRepository()
        self.sub_repo = FakeSubmissionRepository()
        self.service = ChallengeService(self.post_repo, self.sub_repo)

    def test_create_challenge_returns_id(self):
        result = self.service.create_challenge("7-Day Focus Sprint")
        self.assertIn("id", result)
        self.assertIn("message", result)

    def test_submit_proof_creates_pending_submission(self):
        result = self.service.submit_proof("challenge_1", "user@example.com", 1, "http://img.jpg")
        self.assertEqual(result["status"], "success")
        self.assertIn("submission_id", result)

    def test_moderate_submission_approved(self):
        self.service.submit_proof("chal_1", "user@example.com", 1, "http://img.jpg")
        sub_id = "1"
        result = self.service.moderate_submission(sub_id, "approved")
        self.assertEqual(result["status"], "success")

    def test_moderate_invalid_status_returns_error(self):
        result = self.service.moderate_submission("1", "maybe")
        self.assertEqual(result["status"], "error")

    def test_get_leaderboard_empty_challenge(self):
        result = self.service.get_leaderboard("empty_challenge")
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["data"], [])

    def test_get_submissions_returns_list(self):
        self.service.submit_proof("chal_x", "a@example.com", 1, "http://img.jpg")
        self.service.submit_proof("chal_x", "b@example.com", 1, "http://img2.jpg")
        result = self.service.get_submissions("chal_x")
        self.assertEqual(result["status"], "success")
        self.assertEqual(len(result["data"]), 2)


if __name__ == "__main__":
    unittest.main()
