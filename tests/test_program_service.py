import unittest

from backend.business_logic.services.program_service import ProgramService, _get_phase_for_day


class FakeProgramRepository:
    def __init__(self):
        self._store = []

    def find_active(self, email):
        for p in self._store:
            if p["email"] == email and p.get("status") == "active":
                return p
        return None

    def find_by_email(self, email):
        return [p for p in self._store if p["email"] == email]

    def insert(self, data):
        self._store.append(data.copy())

    def upsert_active(self, email, data):
        for p in self._store:
            if p["email"] == email and p.get("status") == "active":
                p.update(data)
                return
        self._store.append({"email": email, **data})


class PhaseMapTests(unittest.TestCase):
    def test_day_1_is_start(self):
        self.assertEqual(_get_phase_for_day(1), "START")

    def test_day_7_is_start(self):
        self.assertEqual(_get_phase_for_day(7), "START")

    def test_day_8_is_rhythm(self):
        self.assertEqual(_get_phase_for_day(8), "RHYTHM")

    def test_day_21_is_rhythm(self):
        self.assertEqual(_get_phase_for_day(21), "RHYTHM")

    def test_day_22_is_reinforcement(self):
        self.assertEqual(_get_phase_for_day(22), "REINFORCEMENT")

    def test_day_30_is_reinforcement(self):
        self.assertEqual(_get_phase_for_day(30), "REINFORCEMENT")


class ProgramServiceTests(unittest.TestCase):
    def setUp(self):
        self.repo = FakeProgramRepository()
        self.service = ProgramService(self.repo)
        self.email = "test@example.com"

    def test_start_program_creates_active_program(self):
        result = self.service.start_program(self.email, "focus_productivity", "beginner")
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["data"]["current_day"], 1)
        self.assertEqual(result["data"]["current_phase"], "START")
        self.assertEqual(result["data"]["status"], "active")

    def test_start_program_invalid_level_returns_error(self):
        result = self.service.start_program(self.email, "focus_productivity", "expert")
        self.assertEqual(result["status"], "error")

    def test_start_program_duplicate_returns_error(self):
        self.service.start_program(self.email, "focus_productivity", "beginner")
        result = self.service.start_program(self.email, "studying", "medium")
        self.assertEqual(result["status"], "error")
        self.assertIn("already have", result["message"])

    def test_get_status_returns_active_program(self):
        self.service.start_program(self.email, "studying", "medium")
        result = self.service.get_status(self.email)
        self.assertEqual(result["status"], "success")
        self.assertIsNotNone(result["data"])
        self.assertIn("today_tasks", result["data"])

    def test_complete_day_advances_day(self):
        self.service.start_program(self.email, "studying", "beginner")
        result = self.service.complete_day(self.email)
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["data"]["current_day"], 2)

    def test_complete_day_no_program_returns_error(self):
        result = self.service.complete_day("nobody@example.com")
        self.assertEqual(result["status"], "error")

    def test_get_phases_returns_three_phases(self):
        result = self.service.get_phases()
        self.assertEqual(result["status"], "success")
        self.assertEqual(len(result["data"]), 3)
        phase_names = [p["name"] for p in result["data"]]
        self.assertIn("START", phase_names)
        self.assertIn("RHYTHM", phase_names)
        self.assertIn("REINFORCEMENT", phase_names)


if __name__ == "__main__":
    unittest.main()
