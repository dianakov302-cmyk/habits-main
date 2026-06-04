import unittest
from datetime import date

from backend.business_logic.services.daily_protocol_service import DailyProtocolService


class FakeDailyProtocolRepository:
    def __init__(self):
        self._store: dict[tuple, dict] = {}

    def find_by_email_and_date(self, email, date_str):
        return self._store.get((email, date_str))

    def upsert(self, email, date_str, data):
        key = (email, date_str)
        if key not in self._store:
            self._store[key] = {"email": email, "date": date_str}
        doc = self._store[key]
        for k, v in data.items():
            if "." in k:
                parts = k.split(".")
                target = doc
                for part in parts[:-1]:
                    target = target.setdefault(part, {})
                target[parts[-1]] = v
            else:
                doc[k] = v

    def find_recent(self, email, limit=30):
        return [v for (e, d), v in self._store.items() if e == email][:limit]


class DailyProtocolServiceTests(unittest.TestCase):
    def setUp(self):
        self.repo = FakeDailyProtocolRepository()
        self.service = DailyProtocolService(self.repo)
        self.email = "test@example.com"
        self.today = date.today().isoformat()

    def test_get_today_returns_none_when_no_protocol(self):
        result = self.service.get_today(self.email)
        self.assertEqual(result["status"], "success")
        self.assertIsNone(result["data"])

    def test_create_protocol_stores_tasks(self):
        result = self.service.create_protocol(
            self.email, self.today, "Meditate 5 min", "Pomodoro session", "Cold shower"
        )
        self.assertEqual(result["status"], "success")
        data = result["data"]
        self.assertEqual(data["minimum_task"]["title"], "Meditate 5 min")
        self.assertFalse(data["minimum_task"]["completed"])
        self.assertEqual(data["points_earned"], 0)

    def test_create_protocol_duplicate_returns_error(self):
        self.service.create_protocol(self.email, self.today, "A", "B", "C")
        result = self.service.create_protocol(self.email, self.today, "A", "B", "C")
        self.assertEqual(result["status"], "error")

    def test_complete_minimum_awards_1_point(self):
        self.service.create_protocol(self.email, self.today, "A", "B", "C")
        result = self.service.complete_task(self.email, self.today, "minimum")
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["data"]["points_earned"], 1)
        self.assertTrue(result["data"]["streak_counts"])

    def test_complete_all_tasks_awards_6_points(self):
        self.service.create_protocol(self.email, self.today, "A", "B", "C")
        self.service.complete_task(self.email, self.today, "minimum")
        self.service.complete_task(self.email, self.today, "target")
        result = self.service.complete_task(self.email, self.today, "bonus")
        self.assertEqual(result["data"]["points_earned"], 6)

    def test_complete_invalid_task_type_returns_error(self):
        self.service.create_protocol(self.email, self.today, "A", "B", "C")
        result = self.service.complete_task(self.email, self.today, "invalid_type")
        self.assertEqual(result["status"], "error")

    def test_streak_does_not_count_without_minimum(self):
        self.service.create_protocol(self.email, self.today, "A", "B", "C")
        result = self.service.complete_task(self.email, self.today, "bonus")
        self.assertFalse(result["data"]["streak_counts"])


if __name__ == "__main__":
    unittest.main()
