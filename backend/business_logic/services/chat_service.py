from datetime import datetime, timezone
from typing import Any

from backend.repositories.chat_repository import AI_COACH_EMAIL, ChatRepository
from backend.repositories.user_repository import UserRepository
from backend.business_logic.services.interfaces import IChatService

AI_COACH_WELCOME = (
    "I'm your coach here. Bring me the obstacle, the excuse, or the goal, and I'll "
    "help you turn it into the next move."
)


class ChatService(IChatService):
    def __init__(self, chat_repository: ChatRepository, user_repository: UserRepository):
        self.chat_repository = chat_repository
        self.user_repository = user_repository

    def get_conversations(self, email: str) -> dict[str, Any]:
        try:
            convs = [
                conv
                for conv in self.chat_repository.find_conversations_for_user(email)
                if conv.get("type") != "coach"
            ]
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

    def get_messages(self, conversation_id: str, sender_email: str | None = None) -> dict[str, Any]:
        try:
            if conversation_id == "coach":
                if not sender_email:
                    return {"status": "error", "message": "Conversation not found."}
                conv = self._ensure_coach_conversation(sender_email)
                messages = self.chat_repository.find_messages(conv["_id"])
                return {"status": "success", "data": messages}
            messages = self.chat_repository.find_messages(conversation_id)
            return {"status": "success", "data": messages}
        except Exception as e:
            return {"status": "error", "message": f"Failed to fetch messages: {str(e)}"}

    def send_message(
        self, conversation_id: str, sender_email: str, content: str
    ) -> dict[str, Any]:
        try:
            if conversation_id == "coach":
                conv = self._ensure_coach_conversation(sender_email)
                conversation_id = conv["_id"]
            else:
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
            if conv.get("type") == "coach":
                coach_reply = self._generate_coach_reply(content)
                reply_at = datetime.now(timezone.utc).isoformat()
                self.chat_repository.insert_message(
                    {
                        "conversation_id": conversation_id,
                        "sender_email": AI_COACH_EMAIL,
                        "content": coach_reply,
                        "sent_at": reply_at,
                        "read_by": [AI_COACH_EMAIL],
                    }
                )
                self.chat_repository.update_conversation_last_message(
                    conversation_id, coach_reply, reply_at
                )
            else:
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

    def _ensure_coach_conversation(self, email: str):
        existing = self.chat_repository.find_ai_conversation(email)
        if existing:
            return existing

        now = datetime.now(timezone.utc).isoformat()
        data = {
            "type": "coach",
            "participants": [email, AI_COACH_EMAIL],
            "last_message": AI_COACH_WELCOME,
            "last_message_at": now,
            "challenge_id": None,
        }
        conv_id = self.chat_repository.insert_conversation(data)
        self.chat_repository.insert_message(
            {
                "conversation_id": conv_id,
                "sender_email": AI_COACH_EMAIL,
                "content": AI_COACH_WELCOME,
                "sent_at": now,
                "read_by": [AI_COACH_EMAIL, email],
            }
        )
        return {"_id": conv_id, **data}

    def _generate_coach_reply(self, content: str) -> str:
        text = content.lower()

        if any(word in text for word in ("tired", "drained", "burned out", "exhausted")):
            return (
                "Then shrink the task. Do the smallest useful version now, protect the streak, "
                "and recover on purpose later."
            )

        if any(word in text for word in ("stuck", "procrast", "can't start", "cannot start", "lazy")):
            return (
                "You do not need more motivation. Pick one action you can finish in 10 minutes "
                "and start before you negotiate with yourself."
            )

        if any(word in text for word in ("distract", "scroll", "phone", "noise", "messaging")):
            return (
                "Protect the next 25 minutes: put the phone away, close the extra tabs, and win "
                "the first focused block."
            )

        if any(word in text for word in ("plan", "routine", "schedule", "habit")):
            return (
                "Good. Turn that into one concrete next action for today. Specific beats vague every "
                "single time."
            )

        if content.strip().endswith("?"):
            return (
                "Answer it by choosing the next action, not by overthinking. If you want, send the "
                "obstacle and I'll help you shrink it."
            )

        return (
            "Keep moving. Consistency beats intensity. What is the one move that would make today "
            "a win?"
        )
