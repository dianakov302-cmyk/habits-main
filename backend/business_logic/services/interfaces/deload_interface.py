from abc import ABC, abstractmethod
from typing import Any


class IDeloadService(ABC):
    @abstractmethod
    def get_status(self, email: str) -> dict[str, Any]:
        pass

    @abstractmethod
    def complete_deload(self, email: str, activity: str) -> dict[str, Any]:
        pass

    @abstractmethod
    def get_history(self, email: str) -> dict[str, Any]:
        pass
