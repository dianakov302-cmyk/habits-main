import unittest

from backend.business_logic.services.weekly_review_service import WeeklyReviewService


class FakeWeeklyReviewRepository:
    def __init__(self):
        self._store = []

    def insert(self, data):
        self._store.append(data.copy())

    def find_latest(self, email):
        entries = [e for e in self._store if e["email"] == email]
        return entries[-1] if entries else None

    def find_history(self, email):
        return [e for e in self._store if e["email"] == email]

    def count_recent(self, email, since_iso):
        return len([e for e in self._store if e["email"] == email])


class WeeklyReviewServiceTests(unittest.TestCase):
    def setUp(self):
        self.repo = FakeWeeklyReviewRepository()
        self.service = WeeklyReviewService(self.repo)
        self.email = "test@example.com"

    def test_submit_review_stores_and_returns_suggestions(self):
        result = self.service.submit_review(
            self.email,
            what_worked="Morning routine",
            what_distracted="Social media scrolling on phone",
            what_to_change="Set a screen curfew",
        )
        self.assertEqual(result["status"], "success")
        self.assertIn("suggestions", result["data"])
        self.assertIn("reflection", result["data"])
        self.assertIsInstance(result["data"]["suggestions"], list)
        self.assertGreater(len(result["data"]["suggestions"]), 0)

    def test_phone_keyword_triggers_digital_suggestion(self):
        result = self.service.submit_review(
            self.email, "Reading books", "phone distractions", "less phone time"
        )
        suggestions = result["data"]["suggestions"]
        phone_suggestion = any("digital" in s.lower() or "phone" in s.lower() for s in suggestions)
        self.assertTrue(phone_suggestion)

    def test_get_latest_returns_most_recent(self):
        self.service.submit_review(self.email, "A", "B", "C")
        self.service.submit_review(self.email, "D", "E", "F")
        result = self.service.get_latest(self.email)
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["data"]["what_worked"], "D")

    def test_get_latest_no_reviews_returns_error(self):
        result = self.service.get_latest("nobody@example.com")
        self.assertEqual(result["status"], "error")

    def test_get_history_returns_all(self):
        self.service.submit_review(self.email, "A", "B", "C")
        self.service.submit_review(self.email, "D", "E", "F")
        result = self.service.get_history(self.email)
        self.assertEqual(len(result["data"]), 2)


if __name__ == "__main__":
    unittest.main()
