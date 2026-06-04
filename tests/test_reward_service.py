import unittest

from backend.business_logic.services.reward_service import RewardService


class FakeRewardRepository:
    def __init__(self):
        self._store: dict[str, dict] = {}

    def find_by_email(self, email):
        return self._store.get(email)

    def upsert(self, email, data):
        if email not in self._store:
            self._store[email] = {"email": email, "unlocked": [], "unlocked_at": {}}
        self._store[email].update(data)

    def add_unlocked(self, email, reward_code, unlocked_at):
        if email not in self._store:
            self._store[email] = {"email": email, "unlocked": [], "unlocked_at": {}}
        if reward_code not in self._store[email]["unlocked"]:
            self._store[email]["unlocked"].append(reward_code)
        self._store[email]["unlocked_at"][reward_code] = unlocked_at


class RewardServiceTests(unittest.TestCase):
    def setUp(self):
        self.repo = FakeRewardRepository()
        self.service = RewardService(self.repo)
        self.email = "test@example.com"

    def test_catalog_returns_all_rewards(self):
        result = self.service.get_catalog()
        self.assertEqual(result["status"], "success")
        self.assertGreater(len(result["data"]), 0)

    def test_get_user_rewards_empty_for_new_user(self):
        result = self.service.get_user_rewards(self.email)
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["data"]["unlocked"], [])

    def test_7_day_streak_unlocks_avatar_frame(self):
        result = self.service.check_and_unlock(self.email, current_streak=7)
        self.assertEqual(result["status"], "success")
        codes = [r["code"] for r in result["newly_unlocked"]]
        self.assertIn("avatar_frame_7", codes)

    def test_30_day_streak_unlocks_elite_bg(self):
        result = self.service.check_and_unlock(self.email, current_streak=30)
        codes = [r["code"] for r in result["newly_unlocked"]]
        self.assertIn("bg_elite", codes)
        self.assertIn("avatar_frame_7", codes)
        self.assertIn("theme_midnight", codes)

    def test_completed_program_unlocks_badge(self):
        result = self.service.check_and_unlock(self.email, completed_programs=1)
        codes = [r["code"] for r in result["newly_unlocked"]]
        self.assertIn("program_complete", codes)

    def test_no_duplicates_on_second_check(self):
        self.service.check_and_unlock(self.email, current_streak=7)
        result = self.service.check_and_unlock(self.email, current_streak=7)
        self.assertEqual(len(result["newly_unlocked"]), 0)

    def test_activate_unlocked_reward(self):
        self.service.check_and_unlock(self.email, current_streak=7)
        result = self.service.activate_reward(self.email, "avatar_frame_7")
        self.assertEqual(result["status"], "success")

    def test_activate_locked_reward_returns_error(self):
        result = self.service.activate_reward(self.email, "avatar_frame_7")
        self.assertEqual(result["status"], "error")

    def test_activate_unknown_code_returns_error(self):
        result = self.service.activate_reward(self.email, "nonexistent_reward")
        self.assertEqual(result["status"], "error")


if __name__ == "__main__":
    unittest.main()
