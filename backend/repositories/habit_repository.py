from backend.repositories.database import get_collection


class HabitRepository:
    def __init__(self):
        self.collection = get_collection("userHabits")

    def create(self, data):
        return self.collection.insert_one(data)

    def find_by_user(self, user_id):
        return list(self.collection.find({"userId": user_id}))

    def delete(self, habit_id):
        return self.collection.delete_one({"_id": habit_id})
