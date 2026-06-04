import unittest
from unittest.mock import MagicMock

import bcrypt

from backend.business_logic.services.user_service import UserService


# ---------------------------------------------------------------------------
# Fake repository
# ---------------------------------------------------------------------------

class FakeUserRepository:
    """In-memory stub — no MongoDB involved."""

    def __init__(self):
        self.users: dict[str, dict] = {}
        # The real UserService calls self.user_repository.collection.update_one(...)
        # for the plaintext-migration path, so we need a collection mock.
        self.collection = MagicMock()

    def find_by_email(self, email: str):
        return self.users.get(email)

    def create_user(self, user_data: dict):
        self.users[user_data["email"]] = dict(user_data)
        return user_data

    # UserService.get_user_profile uses collection.find_one directly
    def _configure_find_one(self, email: str):
        """Helper: make collection.find_one return the stored user (minus password)."""
        def _find_one(query, projection=None):
            user = self.users.get(query.get("email"))
            if user is None:
                return None
            if projection and projection.get("password") == 0:
                return {k: v for k, v in user.items() if k != "password"}
            return user

        self.collection.find_one.side_effect = _find_one


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestRegisterUser(unittest.TestCase):
    def setUp(self):
        self.repo = FakeUserRepository()
        self.service = UserService(self.repo)

    def test_register_hashes_password(self):
        self.service.register_user("alice@example.com", "plaintext123")
        stored = self.repo.users["alice@example.com"]["password"]
        # Must NOT equal the original plaintext
        self.assertNotEqual(stored, "plaintext123")
        # Must be a valid bcrypt hash
        self.assertTrue(bcrypt.checkpw(b"plaintext123", stored.encode()))

    def test_register_success_returns_success_status(self):
        result = self.service.register_user("bob@example.com", "pass456")
        self.assertEqual(result["status"], "success")

    def test_register_duplicate_email_returns_error(self):
        self.service.register_user("dup@example.com", "pass1")
        result = self.service.register_user("dup@example.com", "pass2")
        self.assertEqual(result["status"], "error")
        self.assertIn("already registered", result["message"])

    def test_register_duplicate_email_does_not_overwrite_first_user(self):
        self.service.register_user("keep@example.com", "first")
        first_hash = self.repo.users["keep@example.com"]["password"]
        self.service.register_user("keep@example.com", "second")
        # Hash must not have changed
        self.assertEqual(self.repo.users["keep@example.com"]["password"], first_hash)

    def test_register_stores_name(self):
        self.service.register_user("named@example.com", "pass", "Alice")
        self.assertEqual(self.repo.users["named@example.com"]["name"], "Alice")

    def test_register_empty_name_stores_empty_string(self):
        self.service.register_user("noname@example.com", "pass")
        self.assertEqual(self.repo.users["noname@example.com"]["name"], "")


class TestLoginUser(unittest.TestCase):
    def setUp(self):
        self.repo = FakeUserRepository()
        self.service = UserService(self.repo)
        # Pre-register a user with a bcrypt hash
        self.email = "carol@example.com"
        self.password = "securepass"
        self.service.register_user(self.email, self.password)

    def test_login_with_correct_password_returns_success(self):
        result = self.service.login_user(self.email, self.password)
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["email"], self.email)

    def test_login_with_wrong_password_returns_error(self):
        result = self.service.login_user(self.email, "wrongpassword")
        self.assertEqual(result["status"], "error")

    def test_login_with_nonexistent_email_returns_error(self):
        result = self.service.login_user("ghost@example.com", "pass")
        self.assertEqual(result["status"], "error")
        self.assertIn("not found", result["message"].lower())

    def test_login_migrates_plaintext_password(self):
        """
        If the DB stores a plaintext password (legacy), login should succeed
        and call collection.update_one to rehash it.
        """
        plaintext_email = "legacy@example.com"
        plaintext_pass = "oldpassword"
        # Inject plaintext directly, bypassing register
        self.repo.users[plaintext_email] = {
            "email": plaintext_email,
            "password": plaintext_pass,
        }

        result = self.service.login_user(plaintext_email, plaintext_pass)

        self.assertEqual(result["status"], "success")
        # update_one should have been called to store the new hash
        self.repo.collection.update_one.assert_called_once()
        call_args = self.repo.collection.update_one.call_args
        # First positional arg is the filter
        self.assertEqual(call_args[0][0], {"email": plaintext_email})


class TestGetUserProfile(unittest.TestCase):
    def setUp(self):
        self.repo = FakeUserRepository()
        self.service = UserService(self.repo)
        self.email = "dave@example.com"
        self.service.register_user(self.email, "pass", "Dave")
        # Wire up the collection mock so get_user_profile can call find_one
        self.repo._configure_find_one(self.email)

    def test_get_profile_returns_user_without_password(self):
        result = self.service.get_user_profile(self.email)
        self.assertEqual(result["status"], "success")
        data = result["data"]
        self.assertNotIn("password", data)
        self.assertEqual(data["email"], self.email)

    def test_get_profile_of_nonexistent_user_returns_error(self):
        self.repo._configure_find_one("nobody@example.com")
        result = self.service.get_user_profile("nobody@example.com")
        self.assertEqual(result["status"], "error")


if __name__ == "__main__":
    unittest.main()
