from datetime import datetime
from backend.repositories.progress_repository import ProgressRepository
from backend.business_logic.services.interfaces import IProgressService


class ProgressService(IProgressService):
    def __init__(self, progress_repository: ProgressRepository):
        self.progress_repository = progress_repository

    def complete_habit(self, user_id: str, habit_id: str):
        try:
            progress = {
                "userId": user_id,
                "habitId": habit_id,
                "date": datetime.utcnow(),
                "completed": True,
            }
            self.progress_repository.create(progress)
            return {"message": "Habit completed"}
        except Exception as e:
            return {"error": f"Failed to complete habit: {str(e)}"}

    def get_user_progress(self, user_id: str):
        try:
            logs = self.progress_repository.find_by_user(user_id)
            for log in logs:
                log["_id"] = str(log["_id"])
            return logs
        except Exception as e:
            print(f"Error fetching progress: {e}")
            return []
