import unittest
from unittest.mock import MagicMock
from bson import ObjectId

from backend.business_logic.services.habit_service import HabitService


# ---------------------------------------------------------------------------
# Fake repository
# ---------------------------------------------------------------------------

class FakeInsertResult:
    def __init__(self, oid=None):
        self.inserted_id = oid or ObjectId()


class FakeDeleteResult:
    def __init__(self, deleted_count=1):
        self.deleted_count = deleted_count


class FakeCollection:
    """Minimal in-memory MongoDB collection replacement."""

    def __init__(self):
        self._store: dict[str, dict] = {}

    def insert_one(self, data: dict):
        oid = ObjectId()
        doc = dict(data)
        doc["_id"] = oid
        self._store[str(oid)] = doc
        return FakeInsertResult(oid)

    def find(self, query=None):
        if not query:
            return list(self._store.values())
        results = []
        for doc in self._store.values():
            match = all(doc.get(k) == v for k, v in query.items())
            if match:
                results.append(doc)
        return results

    def find_one(self, query):
        for doc in self._store.values():
            match = all(doc.get(k) == v for k, v in query.items())
            if match:
                return doc
        return None

    def delete_one(self, query):
        for key, doc in list(self._store.items()):
            match = all(doc.get(k) == v for k, v in query.items())
            if match:
                del self._store[key]
                return FakeDeleteResult(1)
        return FakeDeleteResult(0)


class FakeHabitRepository:
    """Stub with the same interface as HabitRepository."""

    def __init__(self):
        self.collection = FakeCollection()

    def create(self, data: dict):
        return self.collection.insert_one(data)

    def find_by_user(self, user_id: str):
        return self.collection.find({"userId": user_id})

    def delete(self, habit_id: ObjectId):
        return self.collection.delete_one({"_id": habit_id})


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestHabitServiceCreate(unittest.TestCase):
    def setUp(self):
        self.repo = FakeHabitRepository()
        self.service = HabitService(self.repo)

    def test_create_habit_returns_success_message(self):
        result = self.service.create_habit("Exercise", "30 min cardio")
        self.assertIn("message", result)
        self.assertEqual(result["message"], "Habit created")

    def test_create_habit_returns_id(self):
        result = self.service.create_habit("Read", "Read 20 pages")
        self.assertIn("id", result)
        self.assertIsInstance(result["id"], str)
        self.assertTrue(len(result["id"]) > 0)

    def test_create_habit_stores_name_and_description(self):
        self.service.create_habit("Meditate", "10 min daily")
        docs = list(self.repo.collection._store.values())
        self.assertEqual(len(docs), 1)
        self.assertEqual(docs[0]["name"], "Meditate")
        self.assertEqual(docs[0]["description"], "10 min daily")

    def test_create_two_habits_returns_different_ids(self):
        r1 = self.service.create_habit("Habit A", "Desc A")
        r2 = self.service.create_habit("Habit B", "Desc B")
        self.assertNotEqual(r1["id"], r2["id"])


class TestHabitServiceGetAll(unittest.TestCase):
    def setUp(self):
        self.repo = FakeHabitRepository()
        self.service = HabitService(self.repo)

    def test_get_all_habits_returns_list(self):
        self.service.create_habit("H1", "D1")
        self.service.create_habit("H2", "D2")
        result = self.service.get_all_habits()
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)

    def test_get_all_habits_empty_returns_empty_list(self):
        result = self.service.get_all_habits()
        self.assertEqual(result, [])

    def test_get_all_habits_ids_are_strings(self):
        self.service.create_habit("Habit", "Desc")
        habits = self.service.get_all_habits()
        for habit in habits:
            self.assertIsInstance(habit["_id"], str)


class TestHabitServiceDelete(unittest.TestCase):
    def setUp(self):
        self.repo = FakeHabitRepository()
        self.service = HabitService(self.repo)

    def test_delete_habit_removes_from_store(self):
        result = self.service.create_habit("ToDelete", "Will be removed")
        habit_id = result["id"]
        deleted = self.service.delete_habit(habit_id)
        self.assertTrue(deleted)
        self.assertEqual(len(self.repo.collection._store), 0)

    def test_delete_nonexistent_habit_returns_false(self):
        # Use a valid ObjectId that doesn't exist in the store
        fake_id = str(ObjectId())
        deleted = self.service.delete_habit(fake_id)
        self.assertFalse(deleted)

    def test_delete_invalid_id_returns_false(self):
        deleted = self.service.delete_habit("not-a-valid-object-id")
        self.assertFalse(deleted)

    def test_delete_habit_returns_true_on_success(self):
        result = self.service.create_habit("Temp", "Temp desc")
        habit_id = result["id"]
        self.assertTrue(self.service.delete_habit(habit_id))


class TestHabitServiceGetById(unittest.TestCase):
    def setUp(self):
        self.repo = FakeHabitRepository()
        self.service = HabitService(self.repo)

    def test_get_habit_returns_habit_dict(self):
        created = self.service.create_habit("MyHabit", "My desc")
        habit_id = created["id"]
        habit = self.service.get_habit(habit_id)
        self.assertIsNotNone(habit)
        self.assertEqual(habit["name"], "MyHabit")

    def test_get_nonexistent_habit_returns_none(self):
        fake_id = str(ObjectId())
        result = self.service.get_habit(fake_id)
        self.assertIsNone(result)

    def test_get_habit_with_invalid_id_returns_none(self):
        result = self.service.get_habit("bad-id")
        self.assertIsNone(result)

    def test_get_habit_id_is_string(self):
        created = self.service.create_habit("Habit", "Desc")
        habit = self.service.get_habit(created["id"])
        self.assertIsInstance(habit["_id"], str)


if __name__ == "__main__":
    unittest.main()
