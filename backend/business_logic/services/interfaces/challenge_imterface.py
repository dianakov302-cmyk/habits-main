from abc import ABC, abstractmethod
from typing import Any


class IChallengeService(ABC):
    @abstractmethod
    def get_challenges(self) -> list[dict[str, Any]]:
        pass

    @abstractmethod
    def create_challenge(self, title: str) -> dict[str, str]:
        pass

    @abstractmethod
    def update_challenge(self, challenge_id: str, updates: dict) -> dict[str, Any]:
        pass

    @abstractmethod
    def delete_challenge(self, challenge_id: str) -> dict[str, Any]:
        pass

    @abstractmethod
    def register_for_challenge(self, challenge_id: str, user_email: str) -> dict[str, Any]:
        pass

    @abstractmethod
    def get_leaderboard(self, challenge_id: str) -> dict[str, Any]:
        pass

    @abstractmethod
    def submit_proof(self, challenge_id: str, user_email: str, day: int,
                     proof_url: str) -> dict[str, Any]:
        pass

    @abstractmethod
    def get_submissions(self, challenge_id: str) -> dict[str, Any]:
        pass

    @abstractmethod
    def moderate_submission(self, submission_id: str, status: str) -> dict[str, Any]:
        pass
