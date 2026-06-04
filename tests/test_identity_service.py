import unittest

from backend.business_logic.services.identity_service import IdentityService, _resolve_level


class FakeIdentityRepository:
    def __init__(self, existing=None):
        self.existing = existing
        self.upserted = []

    def find_by_email(self, email):
        return self.existing

    def upsert(self, email, data):
        self.upserted.append({"email": email, **data})


class ResolveLevelTests(unittest.TestCase):
    def test_score_0_is_lost(self):
        level, next_level, _ = _resolve_level(0)
        self.assertEqual(level, "Lost")
        self.assertEqual(next_level, "Explorer")

    def test_score_20_is_explorer(self):
        level, next_level, _ = _resolve_level(20)
        self.assertEqual(level, "Explorer")

    def test_score_60_is_disciplined(self):
        level, _, _ = _resolve_level(60)
        self.assertEqual(level, "Disciplined")

    def test_score_90_is_elite(self):
        level, next_level, _ = _resolve_level(90)
        self.assertEqual(level, "Elite")
        self.assertEqual(next_level, "Elite")


class IdentityServiceTests(unittest.TestCase):
    def test_get_profile_returns_existing(self):
        existing = {"identity_score": 55.0, "identity_level": "Builder"}
        repo = FakeIdentityRepository(existing=existing)
        service = IdentityService(repo)
        result = service.get_profile("user@example.com")
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["data"]["identity_level"], "Builder")

    def test_get_profile_recalculates_when_no_data(self):
        repo = FakeIdentityRepository(existing=None)
        service = IdentityService(repo)
        result = service.get_profile("new@example.com")
        self.assertEqual(result["status"], "success")
        self.assertIn("identity_score", result["data"])
        self.assertEqual(result["data"]["identity_score"], 0.0)

    def test_recalculate_saves_level(self):
        repo = FakeIdentityRepository(existing={"streak_score": 80.0, "habit_completion_score": 80.0,
                                                 "protocol_score": 80.0, "weekly_review_score": 80.0,
                                                 "program_score": 80.0})
        service = IdentityService(repo)
        result = service.recalculate("user@example.com")
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["data"]["identity_score"], 80.0)
        self.assertGreaterEqual(len(repo.upserted), 1)


if __name__ == "__main__":
    unittest.main()
