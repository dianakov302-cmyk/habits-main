import unittest
from datetime import date

from backend.business_logic.services.deload_service import DeloadService


class FakeDeloadRepository:
    def __init__(self):
        self._store: dict[tuple, dict] = {}

    def find_by_email_and_date(self, email, date_str):
        return self._store.get((email, date_str))

    def find_active(self, email):
        for (e, d), v in self._store.items():
            if e == email and not v.get("completed", True):
                return v
        return None

    def upsert(self, email, date_str, data):
        key = (email, date_str)
        if key not in self._store:
            self._store[key] = {"email": email, "date": date_str}
        self._store[key].update(data)

    def find_history(self, email):
        return [v for (e, d), v in self._store.items() if e == email]


class DeloadServiceTests(unittest.TestCase):
    def setUp(self):
        self.repo = FakeDeloadRepository()
        self.service = DeloadService(self.repo)
        self.email = "test@example.com"
        self.today = date.today().isoformat()

    def test_get_status_returns_inactive_when_no_deload(self):
        result = self.service.get_status(self.email)
        self.assertEqual(result["status"], "success")
        self.assertFalse(result["data"]["active"])

    def test_create_deload_day_stores_entry(self):
        result = self.service.create_deload_day(self.email, 7)
        self.assertEqual(result["status"], "success")
        self.assertFalse(result["data"]["completed"])
        self.assertEqual(result["data"]["trigger_streak"], 7)

    def test_get_status_active_after_creation(self):
        self.service.create_deload_day(self.email, 7)
        result = self.service.get_status(self.email)
        self.assertTrue(result["data"]["active"])
        self.assertIn("activity_options", result["data"])

    def test_complete_deload_with_valid_activity(self):
        self.service.create_deload_day(self.email, 7)
        result = self.service.complete_deload(self.email, "meditation")
        self.assertEqual(result["status"], "success")
        self.assertIn("Meditation", result["activity"])

    def test_complete_deload_invalid_activity(self):
        self.service.create_deload_day(self.email, 7)
        result = self.service.complete_deload(self.email, "yoga")
        self.assertEqual(result["status"], "error")

    def test_complete_deload_no_active_day_returns_error(self):
        result = self.service.complete_deload(self.email, "walk")
        self.assertEqual(result["status"], "error")
        self.assertIn("No active", result["message"])

    def test_history_returns_all_entries(self):
        self.service.create_deload_day(self.email, 7)
        self.service.create_deload_day("other@example.com", 14)
        result = self.service.get_history(self.email)
        self.assertEqual(result["status"], "success")
        self.assertEqual(len(result["data"]), 1)


if __name__ == "__main__":
    unittest.main()
