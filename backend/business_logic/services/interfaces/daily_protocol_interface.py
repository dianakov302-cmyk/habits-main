from abc import ABC, abstractmethod
from typing import Any


class IDailyProtocolService(ABC):
    @abstractmethod
    def get_today(self, email: str) -> dict[str, Any]:
        pass

    @abstractmethod
    def create_protocol(self, email: str, date: str, minimum_task: str,
                        target_task: str, bonus_task: str) -> dict[str, Any]:
        pass

    @abstractmethod
    def complete_task(self, email: str, date: str, task_type: str) -> dict[str, Any]:
        pass

    @abstractmethod
    def get_history(self, email: str, days: int) -> dict[str, Any]:
        pass
