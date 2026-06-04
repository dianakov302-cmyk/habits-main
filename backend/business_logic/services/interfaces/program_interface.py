from abc import ABC, abstractmethod
from typing import Any


class IProgramService(ABC):
    @abstractmethod
    def start_program(self, email: str, goal_code: str, level: str) -> dict[str, Any]:
        pass

    @abstractmethod
    def get_status(self, email: str) -> dict[str, Any]:
        pass

    @abstractmethod
    def complete_day(self, email: str) -> dict[str, Any]:
        pass

    @abstractmethod
    def get_phases(self) -> dict[str, Any]:
        pass
