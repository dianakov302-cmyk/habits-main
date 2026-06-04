from abc import ABC, abstractmethod
from typing import Any


class IProductivityService(ABC):
    # water tracker
    @abstractmethod
    def get_water_log(self, email: str, date: str) -> dict[str, Any]:
        pass

    @abstractmethod
    def log_water(self, email: str, date: str, amount_ml: int) -> dict[str, Any]:
        pass

    @abstractmethod
    def update_water_goal(self, email: str, goal_glasses: int) -> dict[str, Any]:
        pass

    # planner
    @abstractmethod
    def get_planner_tasks(self, email: str, date: str) -> dict[str, Any]:
        pass

    @abstractmethod
    def create_planner_task(self, email: str, date: str, title: str,
                             description: str, priority: str,
                             time_slot: str) -> dict[str, Any]:
        pass

    @abstractmethod
    def update_planner_task(self, task_id: str, updates: dict) -> dict[str, Any]:
        pass

    @abstractmethod
    def delete_planner_task(self, task_id: str) -> dict[str, Any]:
        pass

    @abstractmethod
    def complete_planner_task(self, task_id: str) -> dict[str, Any]:
        pass

    # spaced repetition
    @abstractmethod
    def get_sr_cards(self, email: str) -> dict[str, Any]:
        pass

    @abstractmethod
    def get_sr_due(self, email: str) -> dict[str, Any]:
        pass

    @abstractmethod
    def create_sr_card(self, email: str, deck: str, front: str,
                       back: str) -> dict[str, Any]:
        pass

    @abstractmethod
    def review_sr_card(self, card_id: str, ease: int) -> dict[str, Any]:
        pass

    @abstractmethod
    def delete_sr_card(self, card_id: str) -> dict[str, Any]:
        pass

    # brainstorm
    @abstractmethod
    def get_brainstorm_sessions(self, email: str) -> dict[str, Any]:
        pass

    @abstractmethod
    def create_brainstorm_session(self, email: str, title: str,
                                   tags: list[str]) -> dict[str, Any]:
        pass

    @abstractmethod
    def add_brainstorm_idea(self, session_id: str, content: str) -> dict[str, Any]:
        pass

    @abstractmethod
    def delete_brainstorm_session(self, session_id: str) -> dict[str, Any]:
        pass
