from bson import ObjectId
from bson.errors import InvalidId

from backend.repositories.database import get_collection

AI_COACH_EMAIL = "coach@anaida.space"


class ChatRepository:
    def __init__(self):
        self.conversations = get_collection("conversations")
        self.messages = get_collection("messages")

    # --- conversations ---

    def find_conversations_for_user(self, email: str):
        cursor = self.conversations.find(
            {"participants": email}, {"_id": 1, "participants": 1,
                                      "last_message": 1, "last_message_at": 1,
                                      "challenge_id": 1, "type": 1}
        ).sort("last_message_at", -1)
        docs = list(cursor)
        for doc in docs:
            doc["_id"] = str(doc["_id"])
        return docs

    def find_conversation_by_id(self, conversation_id: str):
        try:
            oid = ObjectId(conversation_id)
        except InvalidId:
            return None
        doc = self.conversations.find_one({"_id": oid})
        if doc:
            doc["_id"] = str(doc["_id"])
        return doc

    def find_dm_conversation(self, email_a: str, email_b: str):
        doc = self.conversations.find_one(
            {
                "type": "dm",
                "participants": {"$all": [email_a, email_b], "$size": 2},
            }
        )
        if doc:
            doc["_id"] = str(doc["_id"])
        return doc

    def find_ai_conversation(self, email: str):
        doc = self.conversations.find_one(
            {
                "type": "coach",
                "participants": {"$all": [email, AI_COACH_EMAIL], "$size": 2},
            }
        )
        if doc:
            doc["_id"] = str(doc["_id"])
        return doc

    def find_challenge_conversation(self, challenge_id: str):
        doc = self.conversations.find_one(
            {"type": "challenge", "challenge_id": challenge_id}
        )
        if doc:
            doc["_id"] = str(doc["_id"])
        return doc

    def insert_conversation(self, data: dict) -> str:
        result = self.conversations.insert_one(data)
        return str(result.inserted_id)

    def update_conversation_last_message(
        self, conversation_id: str, text: str, sent_at: str
    ):
        try:
            oid = ObjectId(conversation_id)
        except InvalidId:
            return
        self.conversations.update_one(
            {"_id": oid},
            {"$set": {"last_message": text, "last_message_at": sent_at}},
        )

    # --- messages ---

    def find_messages(self, conversation_id: str, limit: int = 50):
        cursor = (
            self.messages.find(
                {"conversation_id": conversation_id}, {"_id": 1, "conversation_id": 1,
                                                        "sender_email": 1, "content": 1,
                                                        "sent_at": 1, "read_by": 1}
            )
            .sort("sent_at", 1)
            .limit(limit)
        )
        docs = list(cursor)
        for doc in docs:
            doc["_id"] = str(doc["_id"])
        return docs

    def insert_message(self, data: dict) -> str:
        result = self.messages.insert_one(data)
        return str(result.inserted_id)
