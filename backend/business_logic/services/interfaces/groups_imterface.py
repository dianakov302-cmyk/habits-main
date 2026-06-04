from abc import ABC, abstractmethod
from typing import Any


class IGroupService(ABC):
    @abstractmethod
    def get_groups(self) -> list[dict[str, Any]]:
        pass

    @abstractmethod
    def create_group(self, name: str) -> dict[str, str]:
        pass

    @abstractmethod
    def join_group(self, group_id: str, user_id: str) -> bool:
        pass
