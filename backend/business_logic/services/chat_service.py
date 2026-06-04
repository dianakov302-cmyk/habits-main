from datetime import datetime, timezone
from typing import Any

from backend.repositories.chat_repository import ChatRepository
from backend.repositories.user_repository import UserRepository
from backend.business_logic.services.interfaces import IChatService


class ChatService(IChatService):
    def __init__(self, chat_repository: ChatRepository, user_repository: UserRepository):
        self.chat_repository = chat_repository
        self.user_repository = user_repository

    def get_conversations(self, email: str) -> dict[str, Any]:
        try:
            convs = self.chat_repository.find_conversations_for_user(email)
            return {"status": "success", "data": convs}
        except Exception as e:
            return {"status": "error", "message": f"Failed to fetch conversations: {str(e)}"}

    def start_dm(self, sender_email: str, recipient_email: str) -> dict[str, Any]:
        try:
            if sender_email == recipient_email:
                return {"status": "error", "message": "Cannot start a conversation with yourself."}

            recipient = self.user_repository.find_by_email(recipient_email)
            if not recipient:
                return {"status": "error", "message": "Recipient not found."}

            existing = self.chat_repository.find_dm_conversation(sender_email, recipient_email)
            if existing:
                return {"status": "success", "data": existing, "message": "Conversation already exists."}

            now = datetime.now(timezone.utc).isoformat()
            data = {
                "type": "dm",
                "participants": [sender_email, recipient_email],
                "last_message": None,
                "last_message_at": now,
                "challenge_id": None,
            }
            conv_id = self.chat_repository.insert_conversation(data)
            return {
                "status": "success",
                "data": {"_id": conv_id, **data},
                "message": "Conversation started.",
            }
        except Exception as e:
            return {"status": "error", "message": f"Failed to start conversation: {str(e)}"}

    def get_messages(self, conversation_id: str) -> dict[str, Any]:
        try:
            messages = self.chat_repository.find_messages(conversation_id)
            return {"status": "success", "data": messages}
        except Exception as e:
            return {"status": "error", "message": f"Failed to fetch messages: {str(e)}"}

    def send_message(
        self, conversation_id: str, sender_email: str, content: str
    ) -> dict[str, Any]:
        try:
            conv = self.chat_repository.find_conversation_by_id(conversation_id)
            if not conv:
                return {"status": "error", "message": "Conversation not found."}
            if sender_email not in conv.get("participants", []):
                return {"status": "error", "message": "You are not a participant in this conversation."}

            now = datetime.now(timezone.utc).isoformat()
            msg_data = {
                "conversation_id": conversation_id,
                "sender_email": sender_email,
                "content": content,
                "sent_at": now,
                "read_by": [sender_email],
            }
            msg_id = self.chat_repository.insert_message(msg_data)
            self.chat_repository.update_conversation_last_message(
                conversation_id, content, now
            )
            return {
                "status": "success",
                "data": {"_id": msg_id, **msg_data},
            }
        except Exception as e:
            return {"status": "error", "message": f"Failed to send message: {str(e)}"}

    def search_users(self, query: str) -> dict[str, Any]:
        try:
            if len(query) < 2:
                return {"status": "error", "message": "Query must be at least 2 characters."}
            results = list(
                self.user_repository.collection.find(
                    {
                        "$or": [
                            {"email": {"$regex": query, "$options": "i"}},
                            {"name": {"$regex": query, "$options": "i"}},
                        ]
                    },
                    {"_id": 0, "email": 1, "name": 1},
                ).limit(20)
            )
            return {"status": "success", "data": results}
        except Exception as e:
            return {"status": "error", "message": f"Search failed: {str(e)}"}
