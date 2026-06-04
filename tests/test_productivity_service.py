import unittest
from datetime import date

from backend.business_logic.services.productivity_service import ProductivityService, _sm2


class FakeProductivityRepository:
    def __init__(self):
        self._water: dict[tuple, dict] = {}
        self._planner: dict[str, dict] = {}
        self._sr: dict[str, dict] = {}
        self._brainstorm: dict[str, dict] = {}
        self._counter = 0

    def _next_id(self):
        self._counter += 1
        return str(self._counter)

    def find_water_log(self, email, date_str):
        return self._water.get((email, date_str))

    def upsert_water_log(self, email, date_str, data):
        key = (email, date_str)
        if key not in self._water:
            self._water[key] = {"email": email, "date": date_str, "glasses": 0, "goal": 8, "logs": []}
        self._water[key].update(data)

    def push_water_entry(self, email, date_str, entry):
        key = (email, date_str)
        if key not in self._water:
            self._water[key] = {"email": email, "date": date_str, "glasses": 0, "goal": 8, "logs": []}
        self._water[key]["logs"].append(entry)
        self._water[key]["glasses"] += 1

    def find_planner_tasks(self, email, date_str):
        return [t for t in self._planner.values() if t["email"] == email and t["date"] == date_str]

    def insert_planner_task(self, data):
        tid = self._next_id()
        self._planner[tid] = {"_id": tid, **data}
        return tid

    def update_planner_task(self, task_id, updates):
        if task_id not in self._planner:
            class R:
                matched_count = 0
            return R()
        self._planner[task_id].update(updates)
        class R:
            matched_count = 1
        return R()

    def delete_planner_task(self, task_id):
        if task_id not in self._planner:
            class R:
                deleted_count = 0
            return R()
        del self._planner[task_id]
        class R:
            deleted_count = 1
        return R()

    def find_sr_cards(self, email):
        return [c for c in self._sr.values() if not email or c["email"] == email]

    def find_sr_cards_due(self, email, today):
        return [c for c in self._sr.values() if c["email"] == email and c["next_review_date"] <= today]

    def insert_sr_card(self, data):
        cid = self._next_id()
        self._sr[cid] = {"_id": cid, **data}
        return cid

    def update_sr_card(self, card_id, updates):
        if card_id in self._sr:
            self._sr[card_id].update(updates)
            class R:
                matched_count = 1
            return R()
        return None

    def delete_sr_card(self, card_id):
        if card_id not in self._sr:
            class R:
                deleted_count = 0
            return R()
        del self._sr[card_id]
        class R:
            deleted_count = 1
        return R()

    def find_brainstorm_sessions(self, email):
        return [s for s in self._brainstorm.values() if s["email"] == email]

    def insert_brainstorm_session(self, data):
        sid = self._next_id()
        self._brainstorm[sid] = {"_id": sid, **data}
        return sid

    def push_brainstorm_idea(self, session_id, idea, updated_at):
        if session_id not in self._brainstorm:
            class R:
                matched_count = 0
            return R()
        self._brainstorm[session_id]["ideas"].append(idea)
        class R:
            matched_count = 1
        return R()

    def delete_brainstorm_session(self, session_id):
        if session_id not in self._brainstorm:
            class R:
                deleted_count = 0
            return R()
        del self._brainstorm[session_id]
        class R:
            deleted_count = 1
        return R()


class SM2AlgorithmTests(unittest.TestCase):
    def test_ease_1_resets_interval(self):
        _, interval, reps = _sm2(2.5, 10, 5, 1)
        self.assertEqual(interval, 1)
        self.assertEqual(reps, 0)

    def test_ease_4_increases_interval(self):
        _, interval, _ = _sm2(2.5, 1, 1, 4)
        self.assertGreater(interval, 1)

    def test_ease_factor_stays_above_minimum(self):
        ef, _, _ = _sm2(1.3, 1, 0, 1)
        self.assertGreaterEqual(ef, 1.3)


class ProductivityServiceTests(unittest.TestCase):
    def setUp(self):
        self.repo = FakeProductivityRepository()
        self.service = ProductivityService(self.repo)
        self.email = "test@example.com"
        self.today = date.today().isoformat()

    # --- water ---
    def test_log_water_increments_glasses(self):
        self.service.log_water(self.email, self.today, 250)
        result = self.service.get_water_log(self.email, self.today)
        self.assertEqual(result["data"]["glasses"], 1)

    def test_get_water_log_empty_returns_defaults(self):
        result = self.service.get_water_log(self.email, "2020-01-01")
        self.assertEqual(result["data"]["glasses"], 0)
        self.assertEqual(result["data"]["goal"], 8)

    # --- planner ---
    def test_create_planner_task_returns_id(self):
        result = self.service.create_planner_task(self.email, self.today, "Write tests")
        self.assertEqual(result["status"], "success")
        self.assertIn("_id", result["data"])

    def test_complete_planner_task_marks_done(self):
        create = self.service.create_planner_task(self.email, self.today, "Task")
        task_id = create["data"]["_id"]
        result = self.service.complete_planner_task(task_id)
        self.assertEqual(result["status"], "success")

    def test_delete_planner_task(self):
        create = self.service.create_planner_task(self.email, self.today, "Task")
        task_id = create["data"]["_id"]
        result = self.service.delete_planner_task(task_id)
        self.assertEqual(result["status"], "success")

    def test_invalid_priority_returns_error(self):
        result = self.service.create_planner_task(self.email, self.today, "Task", priority="urgent")
        self.assertEqual(result["status"], "error")

    # --- spaced repetition ---
    def test_create_sr_card(self):
        result = self.service.create_sr_card(self.email, "Spanish", "Hola", "Hello")
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["data"]["ease_factor"], 2.5)

    def test_review_sr_card_updates_interval(self):
        create = self.service.create_sr_card(self.email, "Spanish", "Hola", "Hello")
        card_id = create["data"]["_id"]
        result = self.service.review_sr_card(card_id, 3)
        self.assertEqual(result["status"], "success")
        self.assertIn("next_review_date", result)

    def test_review_invalid_ease_returns_error(self):
        create = self.service.create_sr_card(self.email, "Spanish", "Hola", "Hello")
        result = self.service.review_sr_card(create["data"]["_id"], 5)
        self.assertEqual(result["status"], "error")

    # --- brainstorm ---
    def test_create_brainstorm_session(self):
        result = self.service.create_brainstorm_session(self.email, "My Ideas", ["tag1"])
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["data"]["title"], "My Ideas")

    def test_add_idea_to_session(self):
        create = self.service.create_brainstorm_session(self.email, "Ideas")
        sid = create["data"]["_id"]
        result = self.service.add_brainstorm_idea(sid, "Build a rocket")
        self.assertEqual(result["status"], "success")

    def test_delete_brainstorm_session(self):
        create = self.service.create_brainstorm_session(self.email, "Ideas")
        sid = create["data"]["_id"]
        result = self.service.delete_brainstorm_session(sid)
        self.assertEqual(result["status"], "success")


if __name__ == "__main__":
    unittest.main()
