from bson import ObjectId
from bson.errors import InvalidId
from backend.repositories.groups_repository import GroupRepository
from backend.business_logic.services.interfaces import IGroupService


class GroupService(IGroupService):
    def __init__(self, group_repository: GroupRepository):
        self.group_repository = group_repository

    def get_groups(self):
        try:
            groups = self.group_repository.find_all()
            for group in groups:
                group["_id"] = str(group["_id"])
            return groups
        except Exception as e:
            # Return empty list if database is unavailable
            print(f"Error fetching groups: {e}")
            return []

    def create_group(self, name: str):
        try:
            group = {"name": name, "members": []}
            result = self.group_repository.collection.insert_one(group)
            return {"message": "Group created", "id": str(result.inserted_id)}
        except Exception as e:
            return {"error": f"Failed to create group: {str(e)}"}

    def join_group(self, group_id: str, user_id: str):
        try:
            object_id = ObjectId(group_id)
        except InvalidId:
            return False

        try:
            result = self.group_repository.join_group(user_id, object_id)
            return result.matched_count > 0
        except Exception as e:
            print(f"Error joining group: {e}")
            return False
