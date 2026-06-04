from abc import ABC, abstractmethod
from typing import Any


class IWeeklyReviewService(ABC):
    @abstractmethod
    def submit_review(self, email: str, what_worked: str,
                      what_distracted: str, what_to_change: str) -> dict[str, Any]:
        pass

    @abstractmethod
    def get_history(self, email: str) -> dict[str, Any]:
        pass

    @abstractmethod
    def get_latest(self, email: str) -> dict[str, Any]:
        pass
