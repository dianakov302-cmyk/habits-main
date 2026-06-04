from backend.repositories.database import get_collection


class GroupRepository:
    def __init__(self):
        self.collection = get_collection("groups")

    def find_all(self):
        return list(self.collection.find())

    def join_group(self, user_id, group_id):
        return self.collection.update_one(
            {"_id": group_id},
            {"$addToSet": {"members": user_id}}
        )

    def leave_group(self, user_id, group_id):
        return self.collection.update_one(
            {"_id": group_id},
            {"$pull": {"members": user_id}}
        )
