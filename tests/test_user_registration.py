import unittest
from unittest.mock import patch

from backend.business_logic.services.user_service import UserService
from backend.repositories.user_repository import UserRepository


class FakeInsertResult:
    def __init__(self, inserted_id="fake-id"):
        self.inserted_id = inserted_id


class FakeCollection:
    def __init__(self, existing_users=None):
        self.existing_users = existing_users or {}
        self.inserted_documents = []
        self.find_queries = []

    def find_one(self, query, projection=None):
        self.find_queries.append((query, projection))
        return self.existing_users.get(query.get("email"))

    def insert_one(self, document):
        self.inserted_documents.append(document.copy())
        return FakeInsertResult()


class FakeUserRepository:
    def __init__(self, existing_user=None):
        self.existing_user = existing_user
        self.created_users = []

    def find_by_email(self, email):
        if self.existing_user and self.existing_user.get("email") == email:
            return self.existing_user
        return None

    def create_user(self, user_data):
        self.created_users.append(user_data.copy())
        return FakeInsertResult()


class UserRegistrationTests(unittest.TestCase):
    def test_service_register_user_calls_repository_create_user(self):
        repo = FakeUserRepository()
        service = UserService(repo)

        result = service.register_user("new-user@example.com", "secret123", "New User")

        self.assertEqual(result["status"], "success")
        self.assertEqual(len(repo.created_users), 1)
        self.assertEqual(repo.created_users[0]["email"], "new-user@example.com")
        self.assertEqual(repo.created_users[0]["name"], "New User")

    def test_repository_create_user_inserts_into_users_collection(self):
        users_collection = FakeCollection()
        quiz_collection = FakeCollection()

        with patch(
            "backend.repositories.user_repository.get_collection",
            side_effect=[users_collection, quiz_collection],
        ):
            repository = UserRepository()
            repository.create_user(
                {
                    "email": "db-user@example.com",
                    "password": "secret123",
                    "name": "DB User",
                }
            )

        self.assertEqual(len(users_collection.inserted_documents), 1)
        document = users_collection.inserted_documents[0]
        self.assertEqual(document["email"], "db-user@example.com")
        self.assertEqual(document["name"], "DB User")
        self.assertEqual(document["password"], "secret123")
        self.assertEqual(document["auth_provider"], "email")

    def test_service_registration_does_not_write_duplicate_user(self):
        existing_user = {"email": "dup@example.com"}
        repo = FakeUserRepository(existing_user=existing_user)
        service = UserService(repo)

        result = service.register_user("dup@example.com", "secret123", "Dup User")

        self.assertEqual(result["status"], "error")
        self.assertEqual(len(repo.created_users), 0)


if __name__ == "__main__":
    unittest.main()
