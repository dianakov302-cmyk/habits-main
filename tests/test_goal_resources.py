import unittest

from backend.business_logic.services.goal_service import GoalService


class FakeGoalRepository:
    def find_by_email(self, email):
        return None

    def upsert_goal(self, email, data):
        pass


class GoalResourcesTests(unittest.TestCase):
    def setUp(self):
        self.service = GoalService(FakeGoalRepository())

    def test_resources_returned_for_focus_productivity(self):
        result = self.service.get_goal_resources("focus_productivity")
        self.assertEqual(result["status"], "success")
        self.assertEqual(len(result["data"]["books"]), 3)
        self.assertEqual(len(result["data"]["videos"]), 5)

    def test_resources_returned_for_studying(self):
        result = self.service.get_goal_resources("studying")
        self.assertEqual(result["status"], "success")
        titles = [b["title"] for b in result["data"]["books"]]
        self.assertIn("Make It Stick", titles)

    def test_unknown_goal_code_returns_error(self):
        result = self.service.get_goal_resources("unknown_goal")
        self.assertEqual(result["status"], "error")

    def test_recommendations_beginner(self):
        result = self.service.get_habit_recommendations("focus_productivity", "beginner")
        self.assertEqual(result["status"], "success")
        self.assertGreater(len(result["data"]), 0)
        self.assertIn("name", result["data"][0])
        self.assertIn("description", result["data"][0])

    def test_recommendations_invalid_level(self):
        result = self.service.get_habit_recommendations("focus_productivity", "pro")
        self.assertEqual(result["status"], "error")

    def test_recommendations_all_goals_have_entries(self):
        goal_codes = [
            "focus_productivity", "build_discipline", "physical_health",
            "mental_balance", "personal_growth", "social_motivation",
            "life_reset", "studying", "find_people", "find_direction",
        ]
        for code in goal_codes:
            result = self.service.get_habit_recommendations(code, "beginner")
            self.assertEqual(result["status"], "success", f"Failed for goal: {code}")

    def test_resources_all_goals_have_entries(self):
        goal_codes = [
            "focus_productivity", "build_discipline", "physical_health",
            "mental_balance", "personal_growth", "social_motivation",
            "life_reset", "studying", "find_people", "find_direction",
        ]
        for code in goal_codes:
            result = self.service.get_goal_resources(code)
            self.assertEqual(result["status"], "success", f"No resources for: {code}")
            self.assertEqual(len(result["data"]["books"]), 3, f"Need 3 books for: {code}")
            self.assertEqual(len(result["data"]["videos"]), 5, f"Need 5 videos for: {code}")


if __name__ == "__main__":
    unittest.main()
