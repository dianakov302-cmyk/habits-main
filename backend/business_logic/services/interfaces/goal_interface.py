from abc import ABC, abstractmethod
from typing import Any


class IGoalService(ABC):
    @abstractmethod
    def get_goal_options(self) -> dict[str, Any]:
        pass

    @abstractmethod
    def set_goal(self, email: str, goal_code: str) -> dict[str, Any]:
        pass

    @abstractmethod
    def get_user_goal(self, email: str) -> dict[str, Any]:
        pass

    @abstractmethod
    def get_goal_resources(self, goal_code: str) -> dict[str, Any]:
        pass

    @abstractmethod
    def get_habit_recommendations(self, goal_code: str, level: str) -> dict[str, Any]:
        pass
