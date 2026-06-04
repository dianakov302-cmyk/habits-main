import unittest
from bson import ObjectId

from backend.business_logic.services.progress_service import ProgressService


# ---------------------------------------------------------------------------
# Fake repository
# ---------------------------------------------------------------------------

class FakeInsertResult:
    def __init__(self):
        self.inserted_id = ObjectId()


class FakeProgressRepository:
    """In-memory stub for ProgressRepository."""

    def __init__(self):
        self._store: list[dict] = []

    def create(self, data: dict):
        doc = dict(data)
        doc["_id"] = ObjectId()
        self._store.append(doc)
        return FakeInsertResult()

    def find_by_user(self, user_id: str):
        return [dict(doc) for doc in self._store if doc.get("userId") == user_id]


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestProgressServiceCompleteHabit(unittest.TestCase):
    def setUp(self):
        self.repo = FakeProgressRepository()
        self.service = ProgressService(self.repo)

    def test_complete_habit_creates_progress_entry(self):
        self.service.complete_habit("user1", "habit1")
        self.assertEqual(len(self.repo._store), 1)

    def test_complete_habit_returns_success_message(self):
        result = self.service.complete_habit("user1", "habit1")
        self.assertIn("message", result)
        self.assertEqual(result["message"], "Habit completed")

    def test_complete_habit_stores_user_id(self):
        self.service.complete_habit("user_abc", "habit_xyz")
        self.assertEqual(self.repo._store[0]["userId"], "user_abc")

    def test_complete_habit_stores_habit_id(self):
        self.service.complete_habit("user_abc", "habit_xyz")
        self.assertEqual(self.repo._store[0]["habitId"], "habit_xyz")

    def test_complete_habit_stores_completed_true(self):
        self.service.complete_habit("user1", "h1")
        self.assertTrue(self.repo._store[0]["completed"])

    def test_complete_habit_stores_timestamp(self):
        self.service.complete_habit("user1", "h1")
        self.assertIn("date", self.repo._store[0])


class TestProgressServiceGetProgress(unittest.TestCase):
    def setUp(self):
        self.repo = FakeProgressRepository()
        self.service = ProgressService(self.repo)

    def test_get_progress_returns_history_list(self):
        self.service.complete_habit("user1", "habit1")
        self.service.complete_habit("user1", "habit2")
        result = self.service.get_user_progress("user1")
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)

    def test_get_progress_for_new_user_returns_empty(self):
        result = self.service.get_user_progress("newuser")
        self.assertEqual(result, [])

    def test_get_progress_only_returns_own_entries(self):
        self.service.complete_habit("userA", "h1")
        self.service.complete_habit("userB", "h2")
        result = self.service.get_user_progress("userA")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["userId"], "userA")

    def test_get_progress_ids_are_strings(self):
        self.service.complete_habit("user1", "habit1")
        result = self.service.get_user_progress("user1")
        self.assertIsInstance(result[0]["_id"], str)

    def test_multiple_completions_accumulate(self):
        for i in range(5):
            self.service.complete_habit("user1", f"habit{i}")
        result = self.service.get_user_progress("user1")
        self.assertEqual(len(result), 5)


if __name__ == "__main__":
    unittest.main()
