from backend.repositories.database import get_collection


class ProgressRepository:
    def __init__(self):
        self.collection = get_collection("progress")

    def create(self, data):
        return self.collection.insert_one(data)

    def find_by_user(self, user_id):
        return list(self.collection.find({"userId": user_id}))
