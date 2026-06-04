from datetime import date, datetime, timezone, timedelta
from typing import Any

from backend.repositories.productivity_repository import ProductivityRepository
from backend.business_logic.services.interfaces import IProductivityService

# SM-2 spaced repetition algorithm
def _sm2(ease_factor: float, interval: int, repetitions: int, ease: int):
    """
    ease: 1=again, 2=hard, 3=good, 4=easy
    Returns (new_ease_factor, new_interval, new_repetitions)
    """
    if ease < 3:
        repetitions = 0
        interval = 1
    else:
        if repetitions == 0:
            interval = 1
        elif repetitions == 1:
            interval = 6
        else:
            interval = round(interval * ease_factor)
        repetitions += 1

    ease_factor = max(1.3, ease_factor + 0.1 - (5 - ease) * (0.08 + (5 - ease) * 0.02))
    return round(ease_factor, 2), interval, repetitions


class ProductivityService(IProductivityService):
    def __init__(self, productivity_repository: ProductivityRepository):
        self.productivity_repository = productivity_repository

    # --- water tracker ---

    def get_water_log(self, email: str, date_str: str) -> dict[str, Any]:
        try:
            doc = self.productivity_repository.find_water_log(email, date_str)
            if doc is None:
                return {
                    "status": "success",
                    "data": {"email": email, "date": date_str, "glasses": 0, "goal": 8, "logs": []},
                }
            return {"status": "success", "data": doc}
        except Exception as e:
            return {"status": "error", "message": f"Failed to get water log: {str(e)}"}

    def log_water(self, email: str, date_str: str, amount_ml: int = 250) -> dict[str, Any]:
        try:
            now = datetime.now(timezone.utc).strftime("%H:%M")
            entry = {"time": now, "amount_ml": amount_ml}
            self.productivity_repository.push_water_entry(email, date_str, entry)
            doc = self.productivity_repository.find_water_log(email, date_str)
            return {
                "status": "success",
                "message": f"+1 glass logged ({amount_ml}ml).",
                "data": doc,
            }
        except Exception as e:
            return {"status": "error", "message": f"Failed to log water: {str(e)}"}

    def update_water_goal(self, email: str, goal_glasses: int) -> dict[str, Any]:
        try:
            today = date.today().isoformat()
            self.productivity_repository.upsert_water_log(email, today, {"goal": goal_glasses})
            return {"status": "success", "message": f"Water goal set to {goal_glasses} glasses/day."}
        except Exception as e:
            return {"status": "error", "message": f"Failed to update goal: {str(e)}"}

    # --- planner ---

    def get_planner_tasks(self, email: str, date_str: str) -> dict[str, Any]:
        try:
            tasks = self.productivity_repository.find_planner_tasks(email, date_str)
            return {"status": "success", "data": tasks}
        except Exception as e:
            return {"status": "error", "message": f"Failed to get planner tasks: {str(e)}"}

    def create_planner_task(
        self,
        email: str,
        date_str: str,
        title: str,
        description: str = "",
        priority: str = "medium",
        time_slot: str = "",
    ) -> dict[str, Any]:
        try:
            if priority not in ("high", "medium", "low"):
                return {"status": "error", "message": "priority must be: high, medium, or low"}
            now = datetime.now(timezone.utc).isoformat()
            data = {
                "email": email,
                "date": date_str,
                "title": title,
                "description": description,
                "priority": priority,
                "time_slot": time_slot,
                "completed": False,
                "created_at": now,
            }
            task_id = self.productivity_repository.insert_planner_task(data)
            return {"status": "success", "data": {"_id": task_id, **data}}
        except Exception as e:
            return {"status": "error", "message": f"Failed to create task: {str(e)}"}

    def update_planner_task(self, task_id: str, updates: dict) -> dict[str, Any]:
        try:
            allowed = {"title", "description", "priority", "time_slot"}
            safe = {k: v for k, v in updates.items() if k in allowed}
            if not safe:
                return {"status": "error", "message": "No valid fields to update."}
            result = self.productivity_repository.update_planner_task(task_id, safe)
            if result is None or result.matched_count == 0:
                return {"status": "error", "message": "Task not found."}
            return {"status": "success", "message": "Task updated."}
        except Exception as e:
            return {"status": "error", "message": f"Failed to update task: {str(e)}"}

    def delete_planner_task(self, task_id: str) -> dict[str, Any]:
        try:
            result = self.productivity_repository.delete_planner_task(task_id)
            if result is None or result.deleted_count == 0:
                return {"status": "error", "message": "Task not found."}
            return {"status": "success", "message": "Task deleted."}
        except Exception as e:
            return {"status": "error", "message": f"Failed to delete task: {str(e)}"}

    def complete_planner_task(self, task_id: str) -> dict[str, Any]:
        try:
            result = self.productivity_repository.update_planner_task(task_id, {"completed": True})
            if result is None or result.matched_count == 0:
                return {"status": "error", "message": "Task not found."}
            return {"status": "success", "message": "Task marked complete."}
        except Exception as e:
            return {"status": "error", "message": f"Failed to complete task: {str(e)}"}

    # --- spaced repetition ---

    def get_sr_cards(self, email: str) -> dict[str, Any]:
        try:
            cards = self.productivity_repository.find_sr_cards(email)
            return {"status": "success", "data": cards}
        except Exception as e:
            return {"status": "error", "message": f"Failed to get cards: {str(e)}"}

    def get_sr_due(self, email: str) -> dict[str, Any]:
        try:
            today = date.today().isoformat()
            cards = self.productivity_repository.find_sr_cards_due(email, today)
            return {"status": "success", "data": cards, "count": len(cards)}
        except Exception as e:
            return {"status": "error", "message": f"Failed to get due cards: {str(e)}"}

    def create_sr_card(self, email: str, deck: str, front: str, back: str) -> dict[str, Any]:
        try:
            today = date.today().isoformat()
            now = datetime.now(timezone.utc).isoformat()
            data = {
                "email": email,
                "deck": deck,
                "front": front,
                "back": back,
                "ease_factor": 2.5,
                "interval_days": 1,
                "repetitions": 0,
                "next_review_date": today,
                "created_at": now,
            }
            card_id = self.productivity_repository.insert_sr_card(data)
            return {"status": "success", "data": {"_id": card_id, **data}}
        except Exception as e:
            return {"status": "error", "message": f"Failed to create card: {str(e)}"}

    def review_sr_card(self, card_id: str, ease: int) -> dict[str, Any]:
        try:
            if ease not in (1, 2, 3, 4):
                return {"status": "error", "message": "ease must be 1 (again), 2 (hard), 3 (good), or 4 (easy)"}
            find_by_id = getattr(self.productivity_repository, 'find_sr_card_by_id', None)
            if find_by_id:
                card = find_by_id(card_id)
            else:
                card = next(
                    (c for c in self.productivity_repository.find_sr_cards("")
                     if c.get("_id") == card_id),
                    None,
                )
            if card is None:
                return {"status": "error", "message": "Card not found."}

            ef = 2.5
            interval = 1
            reps = 0
            if card:
                ef = card.get("ease_factor", 2.5)
                interval = card.get("interval_days", 1)
                reps = card.get("repetitions", 0)

            new_ef, new_interval, new_reps = _sm2(ef, interval, reps, ease)
            next_date = (date.today() + timedelta(days=new_interval)).isoformat()

            updates = {
                "ease_factor": new_ef,
                "interval_days": new_interval,
                "repetitions": new_reps,
                "next_review_date": next_date,
            }
            self.productivity_repository.update_sr_card(card_id, updates)
            return {
                "status": "success",
                "message": f"Review saved. Next review in {new_interval} day(s).",
                "next_review_date": next_date,
            }
        except Exception as e:
            return {"status": "error", "message": f"Failed to review card: {str(e)}"}

    def delete_sr_card(self, card_id: str) -> dict[str, Any]:
        try:
            result = self.productivity_repository.delete_sr_card(card_id)
            if result is None or result.deleted_count == 0:
                return {"status": "error", "message": "Card not found."}
            return {"status": "success", "message": "Card deleted."}
        except Exception as e:
            return {"status": "error", "message": f"Failed to delete card: {str(e)}"}

    # --- brainstorm ---

    def get_brainstorm_sessions(self, email: str) -> dict[str, Any]:
        try:
            sessions = self.productivity_repository.find_brainstorm_sessions(email)
            return {"status": "success", "data": sessions}
        except Exception as e:
            return {"status": "error", "message": f"Failed to get sessions: {str(e)}"}

    def create_brainstorm_session(
        self, email: str, title: str, tags: list[str] = None
    ) -> dict[str, Any]:
        try:
            now = datetime.now(timezone.utc).isoformat()
            data = {
                "email": email,
                "title": title,
                "ideas": [],
                "tags": tags or [],
                "created_at": now,
                "updated_at": now,
            }
            session_id = self.productivity_repository.insert_brainstorm_session(data)
            return {"status": "success", "data": {"_id": session_id, **data}}
        except Exception as e:
            return {"status": "error", "message": f"Failed to create session: {str(e)}"}

    def add_brainstorm_idea(self, session_id: str, content: str) -> dict[str, Any]:
        try:
            now = datetime.now(timezone.utc).isoformat()
            idea = {"content": content, "added_at": now}
            result = self.productivity_repository.push_brainstorm_idea(session_id, idea, now)
            if result is None or result.matched_count == 0:
                return {"status": "error", "message": "Session not found."}
            return {"status": "success", "message": "Idea added.", "data": idea}
        except Exception as e:
            return {"status": "error", "message": f"Failed to add idea: {str(e)}"}

    def delete_brainstorm_session(self, session_id: str) -> dict[str, Any]:
        try:
            result = self.productivity_repository.delete_brainstorm_session(session_id)
            if result is None or result.deleted_count == 0:
                return {"status": "error", "message": "Session not found."}
            return {"status": "success", "message": "Session deleted."}
        except Exception as e:
            return {"status": "error", "message": f"Failed to delete session: {str(e)}"}
