from abc import ABC, abstractmethod
from typing import Any


class IProgressService(ABC):
    @abstractmethod
    def complete_habit(self, user_id: str, habit_id: str) -> dict[str, str]:
        pass

    @abstractmethod
    def get_user_progress(self, user_id: str) -> list[dict[str, Any]]:
        pass
