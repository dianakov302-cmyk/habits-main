from backend.repositories.database import get_collection


class PostRepository:
    def __init__(self):
        self.collection = get_collection("posts")

    def create(self, data):
        return self.collection.insert_one(data)

    def find_by_group(self, group_id):
        return list(self.collection.find({"groupId": group_id}))

    def delete(self, post_id):
        return self.collection.delete_one({"_id": post_id})
