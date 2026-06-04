from abc import ABC, abstractmethod
from typing import Any


class IUserService(ABC):
    @abstractmethod
    def login_user(self, email: str, password: str) -> dict[str, Any]:
        pass

    @abstractmethod
    def logout_user(self, email: str) -> dict[str, Any]:
        pass

    @abstractmethod
    def register_user(self, email: str, password: str, name: str | None = None) -> dict[str, Any]:
        pass

    @abstractmethod
    def get_user_profile(self, email: str) -> dict[str, Any]:
        pass

    @abstractmethod
    def update_user_profile(
        self,
        email: str,
        new_email: str | None = None,
        new_password: str | None = None,
    ) -> dict[str, Any]:
        pass

    @abstractmethod
    def save_test_result(
        self,
        session_id: str,
        answers: list[str],
        profile: dict[str, Any],
        roadmap: dict[str, Any],
        email: str | None = None,
    ) -> dict[str, Any]:
        pass

