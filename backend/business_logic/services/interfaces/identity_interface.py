from abc import ABC, abstractmethod
from typing import Any


class IIdentityService(ABC):
    @abstractmethod
    def get_profile(self, email: str) -> dict[str, Any]:
        pass

    @abstractmethod
    def recalculate(self, email: str) -> dict[str, Any]:
        pass
