from abc import ABC, abstractmethod
from typing import Any


class IHabitService(ABC):
    @abstractmethod
    def get_all_habits(self) -> list[dict[str, Any]]:
        pass

    @abstractmethod
    def get_habit(self, habit_id: str) -> dict[str, Any] | None:
        pass

    @abstractmethod
    def create_habit(self, name: str, description: str) -> dict[str, str]:
        pass

    @abstractmethod
    def delete_habit(self, habit_id: str) -> bool:
        pass
