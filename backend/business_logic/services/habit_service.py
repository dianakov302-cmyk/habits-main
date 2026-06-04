from bson import ObjectId
from bson.errors import InvalidId
from backend.repositories.habit_repository import HabitRepository
from backend.business_logic.services.interfaces import IHabitService
from datetime import datetime, timedelta


class HabitService(IHabitService):
    def __init__(self, habit_repository: HabitRepository):
        self.habit_repository = habit_repository

    def get_all_habits(self):
        try:
            habits = list(self.habit_repository.collection.find())
            for habit in habits:
                habit["_id"] = str(habit["_id"])
            return habits
        except Exception as e:
            print(f"Error fetching habits: {e}")
            return []

    def get_habit(self, habit_id: str):
        try:
            object_id = ObjectId(habit_id)
        except InvalidId:
            return None

        try:
            habit = self.habit_repository.collection.find_one({"_id": object_id})
            if habit:
                habit["_id"] = str(habit["_id"])
            return habit
        except Exception as e:
            print(f"Error fetching habit: {e}")
            return None

    def create_habit(self, name: str, description: str):
        try:
            result = self.habit_repository.create(
                {
                    "name": name,
                    "description": description,
                }
            )
            return {"message": "Habit created", "id": str(result.inserted_id)}
        except Exception as e:
            return {"error": f"Failed to create habit: {str(e)}"}

    def delete_habit(self, habit_id: str):
        try:
            object_id = ObjectId(habit_id)
        except InvalidId:
            return False

        try:
            result = self.habit_repository.delete(object_id)
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error deleting habit: {e}")
            return False


# В середині класу HabitService
def complete_habit(self, habit_id):
    habit = self.repository.get_by_id(habit_id)  # Отримуємо дані з БД

    today = datetime.combine(datetime.today(), datetime.min.time())
    yesterday = today - timedelta(days=1)

    last_date = habit.get("last_completed_at")
    current_streak = habit.get("current_streak", 0)

    if last_date == today:
        return current_streak  # Вже виконано сьогодні

    if last_date == yesterday:
        new_streak = current_streak + 1
    else:
        new_streak = 1

    # Викликаємо репозиторій для збереження
    self.repository.update_habit_streak(habit_id, new_streak, today)
    return new_streak
