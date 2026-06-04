from abc import ABC, abstractmethod
from typing import Any


class IRewardService(ABC):
    @abstractmethod
    def get_catalog(self) -> dict[str, Any]:
        pass

    @abstractmethod
    def get_user_rewards(self, email: str) -> dict[str, Any]:
        pass

    @abstractmethod
    def check_and_unlock(self, email: str, current_streak: int,
                         completed_programs: int, weekly_reviews: int) -> dict[str, Any]:
        pass

    @abstractmethod
    def activate_reward(self, email: str, reward_code: str) -> dict[str, Any]:
        pass
