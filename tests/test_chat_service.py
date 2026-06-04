import unittest
from unittest.mock import MagicMock

from backend.business_logic.services.chat_service import ChatService


# ---------------------------------------------------------------------------
# Fake repositories
# ---------------------------------------------------------------------------

class FakeChatRepository:
    """In-memory stub for ChatRepository."""

    def __init__(self):
        self._conversations: dict[str, dict] = {}
        self._messages: list[dict] = []
        self._counter = 0

    def _next_id(self) -> str:
        self._counter += 1
        return str(self._counter)

    # --- conversations ---

    def find_conversations_for_user(self, email: str):
        return [
            dict(c) for c in self._conversations.values()
            if email in c.get("participants", [])
        ]

    def find_conversation_by_id(self, conversation_id: str):
        conv = self._conversations.get(conversation_id)
        if conv:
            return dict(conv)
        return None

    def find_dm_conversation(self, email_a: str, email_b: str):
        for conv in self._conversations.values():
            participants = conv.get("participants", [])
            if (
                conv.get("type") == "dm"
                and set(participants) == {email_a, email_b}
            ):
                return dict(conv)
        return None

    def insert_conversation(self, data: dict) -> str:
        conv_id = self._next_id()
        self._conversations[conv_id] = {"_id": conv_id, **data}
        return conv_id

    def update_conversation_last_message(
        self, conversation_id: str, text: str, sent_at: str
    ):
        if conversation_id in self._conversations:
            self._conversations[conversation_id]["last_message"] = text
            self._conversations[conversation_id]["last_message_at"] = sent_at

    # --- messages ---

    def find_messages(self, conversation_id: str, limit: int = 50):
        msgs = [
            dict(m)
            for m in self._messages
            if m["conversation_id"] == conversation_id
        ]
        return msgs[:limit]

    def insert_message(self, data: dict) -> str:
        msg_id = self._next_id()
        self._messages.append({"_id": msg_id, **data})
        return msg_id


class FakeUserRepository:
    """
    In-memory stub for UserRepository.
    ChatService.search_users calls self.user_repository.collection.find(...).limit(20)
    directly, so we must wire collection accordingly.
    """

    def __init__(self):
        self._users: dict[str, dict] = {}
        # Build a mock collection that delegates find() to in-memory data
        self.collection = MagicMock()
        self.collection.find.side_effect = self._collection_find

    def _collection_find(self, query, projection=None):
        """
        Very naive implementation: supports $or with $regex on email/name.
        Returns a mock with .limit() that returns matching docs.
        """
        results = []
        or_clauses = query.get("$or", [])
        for user in self._users.values():
            for clause in or_clauses:
                for field, matcher in clause.items():
                    pattern = matcher.get("$regex", "").lower()
                    if pattern and pattern in user.get(field, "").lower():
                        # Apply projection
                        if projection:
                            doc = {k: user[k] for k in projection if k in user}
                        else:
                            doc = dict(user)
                        results.append(doc)
                        break
                else:
                    continue
                break

        # Return a mock whose .limit() returns the list
        cursor = MagicMock()
        cursor.limit.return_value = results
        return cursor

    def add_user(self, email: str, name: str = ""):
        """Helper to populate the store."""
        self._users[email] = {"email": email, "name": name}

    def find_by_email(self, email: str):
        return self._users.get(email)

    def create_user(self, user_data: dict):
        self._users[user_data["email"]] = dict(user_data)
        return user_data


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestChatServiceConversations(unittest.TestCase):
    def setUp(self):
        self.chat_repo = FakeChatRepository()
        self.user_repo = FakeUserRepository()
        self.service = ChatService(self.chat_repo, self.user_repo)

        # Pre-seed two users
        self.user_repo.add_user("alice@example.com", "Alice")
        self.user_repo.add_user("bob@example.com", "Bob")

    def test_create_conversation_returns_conversation_id(self):
        result = self.service.start_dm("alice@example.com", "bob@example.com")
        self.assertEqual(result["status"], "success")
        self.assertIn("_id", result["data"])

    def test_start_dm_with_self_returns_error(self):
        result = self.service.start_dm("alice@example.com", "alice@example.com")
        self.assertEqual(result["status"], "error")

    def test_start_dm_with_nonexistent_recipient_returns_error(self):
        result = self.service.start_dm("alice@example.com", "ghost@example.com")
        self.assertEqual(result["status"], "error")

    def test_start_dm_twice_returns_existing_conversation(self):
        r1 = self.service.start_dm("alice@example.com", "bob@example.com")
        r2 = self.service.start_dm("alice@example.com", "bob@example.com")
        self.assertEqual(r1["data"]["_id"], r2["data"]["_id"])

    def test_get_conversations_for_user_returns_list(self):
        self.service.start_dm("alice@example.com", "bob@example.com")
        result = self.service.get_conversations("alice@example.com")
        self.assertEqual(result["status"], "success")
        self.assertIsInstance(result["data"], list)
        self.assertGreaterEqual(len(result["data"]), 1)

    def test_get_conversations_empty_for_new_user(self):
        self.user_repo.add_user("newuser@example.com", "New")
        result = self.service.get_conversations("newuser@example.com")
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["data"], [])


class TestChatServiceMessages(unittest.TestCase):
    def setUp(self):
        self.chat_repo = FakeChatRepository()
        self.user_repo = FakeUserRepository()
        self.service = ChatService(self.chat_repo, self.user_repo)

        self.user_repo.add_user("alice@example.com", "Alice")
        self.user_repo.add_user("bob@example.com", "Bob")

        # Create a DM conversation between Alice and Bob
        dm_result = self.service.start_dm("alice@example.com", "bob@example.com")
        self.conv_id = dm_result["data"]["_id"]

    def test_send_message_stores_message(self):
        result = self.service.send_message(self.conv_id, "alice@example.com", "Hello Bob!")
        self.assertEqual(result["status"], "success")
        self.assertIn("_id", result["data"])

    def test_send_message_content_is_preserved(self):
        self.service.send_message(self.conv_id, "alice@example.com", "Hello Bob!")
        msgs = self.chat_repo.find_messages(self.conv_id)
        self.assertEqual(len(msgs), 1)
        self.assertEqual(msgs[0]["content"], "Hello Bob!")

    def test_get_messages_returns_list(self):
        self.service.send_message(self.conv_id, "alice@example.com", "Hi")
        self.service.send_message(self.conv_id, "bob@example.com", "Hey")
        result = self.service.get_messages(self.conv_id)
        self.assertEqual(result["status"], "success")
        self.assertIsInstance(result["data"], list)
        self.assertEqual(len(result["data"]), 2)

    def test_get_messages_empty_conversation(self):
        result = self.service.get_messages(self.conv_id)
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["data"], [])

    def test_send_message_by_non_participant_returns_error(self):
        self.user_repo.add_user("eve@example.com", "Eve")
        result = self.service.send_message(self.conv_id, "eve@example.com", "Snoop")
        self.assertEqual(result["status"], "error")

    def test_send_message_to_nonexistent_conversation_returns_error(self):
        result = self.service.send_message("9999", "alice@example.com", "Hello")
        self.assertEqual(result["status"], "error")


class TestChatServiceSearchUsers(unittest.TestCase):
    def setUp(self):
        self.chat_repo = FakeChatRepository()
        self.user_repo = FakeUserRepository()
        self.service = ChatService(self.chat_repo, self.user_repo)

        self.user_repo.add_user("alice@example.com", "Alice Smith")
        self.user_repo.add_user("bob@example.com", "Bob Jones")
        self.user_repo.add_user("carol@example.com", "Carol Alicia")

    def test_search_users_returns_matching_users(self):
        result = self.service.search_users("alice")
        self.assertEqual(result["status"], "success")
        self.assertIsInstance(result["data"], list)
        # alice@example.com email + Carol Alicia name both contain "alice"
        emails = [u["email"] for u in result["data"]]
        self.assertIn("alice@example.com", emails)

    def test_search_short_query_returns_error(self):
        result = self.service.search_users("a")
        self.assertEqual(result["status"], "error")

    def test_search_no_match_returns_empty_list(self):
        result = self.service.search_users("zzznomatch")
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["data"], [])


if __name__ == "__main__":
    unittest.main()
