from bson import ObjectId
from bson.errors import InvalidId
from datetime import datetime, timezone

from backend.repositories.database import get_collection


class ProductivityRepository:
    def __init__(self):
        self.water = get_collection("water_logs")
        self.planner = get_collection("planner_tasks")
        self.sr_cards = get_collection("sr_cards")
        self.brainstorm = get_collection("brainstorm_sessions")

    # --- water tracker ---

    def find_water_log(self, email: str, date: str):
        return self.water.find_one({"email": email, "date": date}, {"_id": 0})

    def upsert_water_log(self, email: str, date: str, data: dict):
        data["email"] = email
        data["date"] = date
        return self.water.update_one(
            {"email": email, "date": date}, {"$set": data}, upsert=True
        )

    def push_water_entry(self, email: str, date: str, entry: dict):
        return self.water.update_one(
            {"email": email, "date": date},
            {
                "$push": {"logs": entry},
                "$inc": {"glasses": 1},
                "$setOnInsert": {"goal": 8},
            },
            upsert=True,
        )

    # --- planner ---

    def find_planner_tasks(self, email: str, date: str):
        cursor = self.planner.find({"email": email, "date": date})
        docs = list(cursor)
        for d in docs:
            d["_id"] = str(d["_id"])
        return docs

    def insert_planner_task(self, data: dict) -> str:
        result = self.planner.insert_one(data)
        return str(result.inserted_id)

    def update_planner_task(self, task_id: str, updates: dict):
        try:
            oid = ObjectId(task_id)
        except InvalidId:
            return None
        return self.planner.update_one({"_id": oid}, {"$set": updates})

    def delete_planner_task(self, task_id: str):
        try:
            oid = ObjectId(task_id)
        except InvalidId:
            return None
        return self.planner.delete_one({"_id": oid})

    # --- spaced repetition ---

    def find_sr_cards(self, email: str):
        cursor = self.sr_cards.find({"email": email}, {"_id": 1, "email": 1, "deck": 1,
                                                        "front": 1, "back": 1,
                                                        "ease_factor": 1, "interval_days": 1,
                                                        "repetitions": 1, "next_review_date": 1})
        docs = list(cursor)
        for d in docs:
            d["_id"] = str(d["_id"])
        return docs

    def find_sr_cards_due(self, email: str, today: str):
        cursor = self.sr_cards.find(
            {"email": email, "next_review_date": {"$lte": today}},
            {"_id": 1, "deck": 1, "front": 1, "back": 1, "ease_factor": 1,
             "interval_days": 1, "repetitions": 1, "next_review_date": 1},
        )
        docs = list(cursor)
        for d in docs:
            d["_id"] = str(d["_id"])
        return docs

    def insert_sr_card(self, data: dict) -> str:
        result = self.sr_cards.insert_one(data)
        return str(result.inserted_id)

    def update_sr_card(self, card_id: str, updates: dict):
        try:
            oid = ObjectId(card_id)
        except InvalidId:
            return None
        return self.sr_cards.update_one({"_id": oid}, {"$set": updates})

    def delete_sr_card(self, card_id: str):
        try:
            oid = ObjectId(card_id)
        except InvalidId:
            return None
        return self.sr_cards.delete_one({"_id": oid})

    # --- brainstorm ---

    def find_brainstorm_sessions(self, email: str):
        cursor = self.brainstorm.find(
            {"email": email},
            {"_id": 1, "email": 1, "title": 1, "ideas": 1, "tags": 1,
             "created_at": 1, "updated_at": 1},
        ).sort("updated_at", -1)
        docs = list(cursor)
        for d in docs:
            d["_id"] = str(d["_id"])
        return docs

    def insert_brainstorm_session(self, data: dict) -> str:
        result = self.brainstorm.insert_one(data)
        return str(result.inserted_id)

    def push_brainstorm_idea(self, session_id: str, idea: dict, updated_at: str):
        try:
            oid = ObjectId(session_id)
        except InvalidId:
            return None
        return self.brainstorm.update_one(
            {"_id": oid},
            {"$push": {"ideas": idea}, "$set": {"updated_at": updated_at}},
        )

    def delete_brainstorm_session(self, session_id: str):
        try:
            oid = ObjectId(session_id)
        except InvalidId:
            return None
        return self.brainstorm.delete_one({"_id": oid})
