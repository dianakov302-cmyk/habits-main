"""
API integration tests using FastAPI TestClient.

Each test class overrides the relevant service factory via
app.dependency_overrides so no real MongoDB connection is needed.
"""

import unittest
from unittest.mock import MagicMock

import bcrypt
from fastapi.testclient import TestClient

from backend.main import app
from backend.auth import create_access_token
from backend.business_logic.services.user_service import UserService
from backend.business_logic.services.habit_service import HabitService
from backend.business_logic.services.goal_service import GoalService
from backend.business_logic.services.groups_service import GroupService
from backend.business_logic.services.challenge_service import ChallengeService
from backend.business_logic.services.identity_service import IdentityService
from backend.business_logic.services.daily_protocol_service import DailyProtocolService


# ---------------------------------------------------------------------------
# Shared fake stubs
# ---------------------------------------------------------------------------

class _FakeInsertResult:
    def __init__(self):
        from bson import ObjectId
        self.inserted_id = ObjectId()


class _FakeUserRepository:
    def __init__(self):
        self.users: dict[str, dict] = {}
        self.collection = MagicMock()
        # Wire find_one on the mock to delegate to in-memory store
        self.collection.find_one.side_effect = self._find_one_mock

    def _find_one_mock(self, query, projection=None):
        user = self.users.get(query.get("email"))
        if user is None:
            return None
        if projection and projection.get("password") == 0:
            return {k: v for k, v in user.items() if k != "password" and k != "_id"}
        return user

    def find_by_email(self, email: str):
        return self.users.get(email)

    def create_user(self, user_data: dict):
        self.users[user_data["email"]] = dict(user_data)
        return user_data

    def seed_user(self, email: str, password: str, name: str = "Test"):
        """Helper to add a user with a bcrypt-hashed password."""
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        self.users[email] = {"email": email, "password": hashed, "name": name}


class _FakeHabitRepository:
    def __init__(self):
        from bson import ObjectId

        class FakeCol:
            def __init__(self_inner):
                self_inner._store: dict = {}

            def insert_one(self_inner, data):
                from bson import ObjectId as OID
                oid = OID()
                doc = dict(data)
                doc["_id"] = oid
                self_inner._store[str(oid)] = doc
                return _FakeInsertResult()

            def find(self_inner, query=None):
                return list(self_inner._store.values())

            def find_one(self_inner, query):
                for doc in self_inner._store.values():
                    if all(doc.get(k) == v for k, v in query.items()):
                        return doc
                return None

            def delete_one(self_inner, query):
                for key, doc in list(self_inner._store.items()):
                    if all(doc.get(k) == v for k, v in query.items()):
                        del self_inner._store[key]
                        class R:
                            deleted_count = 1
                        return R()
                class R:
                    deleted_count = 0
                return R()

        self.collection = FakeCol()

    def create(self, data):
        return self.collection.insert_one(data)

    def find_by_user(self, user_id):
        return self.collection.find({"userId": user_id})

    def delete(self, habit_id):
        return self.collection.delete_one({"_id": habit_id})


class _FakeGoalRepository:
    def __init__(self):
        self._store: dict = {}

    def upsert_goal(self, email, data):
        self._store[email] = data

    def find_by_email(self, email):
        return self._store.get(email)


class _FakeGroupRepository:
    def __init__(self):
        self._store: list = []
        self.collection = MagicMock()
        self.collection.insert_one.return_value = _FakeInsertResult()

    def find_all(self):
        return list(self._store)

    def join_group(self, user_id, group_id):
        class R:
            matched_count = 0
        return R()


class _FakeChallengeRepository:
    def __init__(self):
        self._store: dict = {}
        self.collection = self

    def find(self, query=None):
        return list(self._store.values())

    def insert_one(self, data):
        from bson import ObjectId
        oid = ObjectId()
        data["_id"] = oid
        self._store[str(oid)] = dict(data)
        class R:
            inserted_id = oid
        return R()

    def create(self, data):
        return self.insert_one(data)

    def update_one(self, query, update, upsert=False):
        class R:
            matched_count = 0
        return R()

    def delete_one(self, query):
        class R:
            deleted_count = 0
        return R()


class _FakeSubmissionRepository:
    def __init__(self):
        self._store: dict = {}
        self._counter = 0

    def insert(self, data):
        self._counter += 1
        sid = str(self._counter)
        self._store[sid] = {"_id": sid, **data}
        return sid

    def find_by_challenge(self, challenge_id):
        return [s for s in self._store.values() if s["challenge_id"] == challenge_id]

    def find_by_user_and_challenge(self, user_email, challenge_id):
        return [
            s for s in self._store.values()
            if s["user_email"] == user_email and s["challenge_id"] == challenge_id
        ]

    def update_status(self, submission_id, status):
        if submission_id not in self._store:
            class R:
                matched_count = 0
            return R()
        self._store[submission_id]["status"] = status
        class R:
            matched_count = 1
        return R()


class _FakeIdentityRepository:
    def __init__(self):
        self._store: dict = {}

    def find_by_email(self, email):
        return self._store.get(email)

    def upsert(self, email, data):
        self._store[email] = data

    def collection(self):
        return MagicMock()


class _FakeDailyProtocolRepository:
    def __init__(self):
        self._store: dict = {}
        self._counter = 0

    def _next_id(self):
        self._counter += 1
        return str(self._counter)

    def find_today(self, email, date_str):
        return self._store.get((email, date_str))

    def insert(self, data):
        pid = self._next_id()
        key = (data["email"], data["date"])
        self._store[key] = {"_id": pid, **data}
        return pid

    def update_task(self, email, date_str, task_type, updates):
        key = (email, date_str)
        if key not in self._store:
            class R:
                matched_count = 0
            return R()
        self._store[key].update(updates)
        class R:
            matched_count = 1
        return R()

    def find_history(self, email, since_date):
        return [v for (e, _), v in self._store.items() if e == email]


# ---------------------------------------------------------------------------
# Helper: get_service factory that always returns the same instance
# ---------------------------------------------------------------------------

def _override(service_instance):
    """Returns a zero-arg callable that yields the given service instance."""
    def _get_service():
        return service_instance
    return _get_service


# ---------------------------------------------------------------------------
# Auth endpoint tests
# ---------------------------------------------------------------------------

class TestAuthEndpoints(unittest.TestCase):
    def setUp(self):
        self.fake_user_repo = _FakeUserRepository()
        self.fake_user_service = UserService(self.fake_user_repo)

        # Override get_user_service on the container used by the live app
        container = app.state.container
        app.dependency_overrides[container.get_user_service] = _override(
            self.fake_user_service
        )
        self.client = TestClient(app, raise_server_exceptions=False)

    def tearDown(self):
        app.dependency_overrides.clear()

    def test_register_new_user_returns_success(self):
        resp = self.client.post(
            "/users/register",
            json={"email": "newuser@test.com", "password": "pass123"},
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["status"], "success")

    def test_register_duplicate_user_returns_error(self):
        payload = {"email": "dup@test.com", "password": "pass123"}
        self.client.post("/users/register", json=payload)
        resp = self.client.post("/users/register", json=payload)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["status"], "error")

    def test_login_valid_credentials_returns_token(self):
        self.fake_user_repo.seed_user("login@test.com", "mypass")
        resp = self.client.post(
            "/users/login",
            json={"email": "login@test.com", "password": "mypass"},
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["status"], "success")
        self.assertIn("access_token", data)

    def test_login_invalid_password_returns_error(self):
        self.fake_user_repo.seed_user("user@test.com", "correctpass")
        resp = self.client.post(
            "/users/login",
            json={"email": "user@test.com", "password": "wrongpass"},
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["status"], "error")

    def test_login_response_contains_access_token(self):
        self.fake_user_repo.seed_user("token@test.com", "pass")
        resp = self.client.post(
            "/users/login",
            json={"email": "token@test.com", "password": "pass"},
        )
        self.assertIn("access_token", resp.json())

    def test_get_me_without_token_returns_401(self):
        resp = self.client.get("/users/me")
        self.assertEqual(resp.status_code, 401)

    def test_get_me_with_valid_token_returns_email(self):
        email = "me@test.com"
        token = create_access_token(email)
        resp = self.client.get(
            "/users/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["email"], email)

    def test_get_profile_without_token_returns_401(self):
        resp = self.client.get("/users/profile")
        self.assertEqual(resp.status_code, 401)

    def test_get_profile_with_valid_token_returns_data(self):
        email = "profile@test.com"
        self.fake_user_repo.seed_user(email, "pass", "Profile User")
        token = create_access_token(email)
        resp = self.client.get(
            "/users/profile",
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["status"], "success")
        self.assertNotIn("password", data.get("data", {}))


# ---------------------------------------------------------------------------
# Protected endpoint tests
# ---------------------------------------------------------------------------

class TestProtectedEndpoints(unittest.TestCase):
    def setUp(self):
        container = app.state.container

        fake_habit_service = HabitService(_FakeHabitRepository())

        app.dependency_overrides[container.get_user_service] = _override(
            UserService(_FakeUserRepository())
        )
        app.dependency_overrides[container.get_habit_service] = _override(
            fake_habit_service
        )
        app.dependency_overrides[container.get_identity_service] = _override(
            IdentityService(_FakeIdentityRepository())
        )
        app.dependency_overrides[container.get_daily_protocol_service] = _override(
            DailyProtocolService(_FakeDailyProtocolRepository())
        )

        self.client = TestClient(app, raise_server_exceptions=False)
        self.token = create_access_token("authed@test.com")
        self.auth_headers = {"Authorization": f"Bearer {self.token}"}

    def tearDown(self):
        app.dependency_overrides.clear()

    def test_habits_list_without_auth_returns_401(self):
        resp = self.client.get("/habits/")
        self.assertEqual(resp.status_code, 401)

    def test_habits_list_with_auth_returns_200(self):
        resp = self.client.get("/habits/", headers=self.auth_headers)
        self.assertEqual(resp.status_code, 200)

    def test_create_habit_without_auth_returns_401(self):
        resp = self.client.post(
            "/habits/create",
            json={"name": "Run", "description": "Run 5k"},
        )
        self.assertEqual(resp.status_code, 401)

    def test_create_habit_with_auth_returns_200(self):
        resp = self.client.post(
            "/habits/create",
            json={"name": "Run", "description": "Run 5k"},
            headers=self.auth_headers,
        )
        self.assertEqual(resp.status_code, 200)

    def test_daily_protocol_without_auth_returns_401(self):
        resp = self.client.get("/protocol/today")
        self.assertEqual(resp.status_code, 401)

    def test_identity_profile_without_auth_returns_401(self):
        resp = self.client.get("/identity/profile")
        self.assertEqual(resp.status_code, 401)


# ---------------------------------------------------------------------------
# Public endpoint tests
# ---------------------------------------------------------------------------

class TestPublicEndpoints(unittest.TestCase):
    def setUp(self):
        container = app.state.container

        app.dependency_overrides[container.get_goal_service] = _override(
            GoalService(_FakeGoalRepository())
        )
        app.dependency_overrides[container.get_group_service] = _override(
            GroupService(_FakeGroupRepository())
        )
        app.dependency_overrides[container.get_challenge_service] = _override(
            ChallengeService(_FakeChallengeRepository(), _FakeSubmissionRepository())
        )

        self.client = TestClient(app, raise_server_exceptions=False)

    def tearDown(self):
        app.dependency_overrides.clear()

    def test_health_check_returns_ok_or_degraded(self):
        resp = self.client.get("/health")
        self.assertEqual(resp.status_code, 200)
        # Status is either "ok" (DB connected) or "degraded" (no DB in test env)
        self.assertIn(resp.json()["status"], ("ok", "degraded"))

    def test_goals_options_is_public(self):
        resp = self.client.get("/goals/options")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["status"], "success")
        self.assertIsInstance(data["data"], list)

    def test_groups_list_is_public(self):
        resp = self.client.get("/groups/")
        self.assertEqual(resp.status_code, 200)
        self.assertIsInstance(resp.json(), list)

    def test_challenges_list_is_public(self):
        resp = self.client.get("/challenges/")
        self.assertEqual(resp.status_code, 200)
        self.assertIsInstance(resp.json(), list)

    def test_root_endpoint_is_public(self):
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("docs", resp.json())


if __name__ == "__main__":
    unittest.main()
