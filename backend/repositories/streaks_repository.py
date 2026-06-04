# Додай цей метод у клас HabitRepository
def update_habit_streak(self, habit_id, new_streak, today_date):
    self.collection.update_one(
        {"_id": habit_id},
        {
            "$set": {
                "current_streak": new_streak,
                "last_completed_at": today_date
            },
            "$max": {"longest_streak": new_streak}
        }
    )