from abc import ABC, abstractmethod
from typing import Any


class IChatService(ABC):
    @abstractmethod
    def get_conversations(self, email: str) -> dict[str, Any]:
        pass

    @abstractmethod
    def start_dm(self, sender_email: str, recipient_email: str) -> dict[str, Any]:
        pass

    @abstractmethod
    def get_messages(self, conversation_id: str) -> dict[str, Any]:
        pass

    @abstractmethod
    def send_message(self, conversation_id: str, sender_email: str,
                     content: str) -> dict[str, Any]:
        pass

    @abstractmethod
    def search_users(self, query: str) -> dict[str, Any]:
        pass
