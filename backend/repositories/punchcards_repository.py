from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime

class LoyaltyRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["punch_cards"]

    async def update_punch(self, user_id: str, card_type: str):
        return await self.collection.find_one_and_update(
            {"user_id": user_id, "card_type": card_type, "punches_earned": {"$lt": 10}},
            {"$inc": {"punches_earned": 1}, "$set": {"last_punch_at": datetime.utcnow()}},
            upsert=True,
            return_document=True
        )

    async def mark_as_completed(self, card_id):
        await self.collection.update_one({"_id": card_id}, {"$set": {"is_completed": True}})