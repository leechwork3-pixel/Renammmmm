import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timedelta
from config import Config

client = AsyncIOMotorClient(Config.DB_URL)
db = client[Config.DB_NAME]
user_col = db["users"]

class Element_Network:

    @staticmethod
    async def set_format_template(user_id, template):
        await user_col.update_one(
            {"_id": user_id},
            {"$set": {"template": template}},
            upsert=True
        )

    @staticmethod
    async def get_format_template(user_id):
        user = await user_col.find_one({"_id": user_id})
        return user.get("template") if user else None

    @staticmethod
    async def toggle_metadata(user_id):
        user = await user_col.find_one({"_id": user_id})
        current = user.get("metadata", False)
        await user_col.update_one(
            {"_id": user_id},
            {"$set": {"metadata": not current}},
            upsert=True
        )
        return not current

    @staticmethod
    async def set_metadata(user_id, field, value):
        await user_col.update_one(
            {"_id": user_id},
            {"$set": {f"meta.{field}": value}},
            upsert=True
        )

    @staticmethod
    async def get_metadata(user_id):
        user = await user_col.find_one({"_id": user_id})
        return user.get("meta", {})

    # === Sequence Mode ===

    @staticmethod
    async def start_sequence(user_id):
        await user_col.update_one(
            {"_id": user_id},
            {"$set": {"sequence": []}},
            upsert=True
        )

    @staticmethod
    async def get_sequence(user_id):
        user = await user_col.find_one({"_id": user_id})
        return user.get("sequence", [])

    @staticmethod
    async def store_sequence_file(user_id, file_name, file_id, caption=None):
        await user_col.update_one(
            {"_id": user_id},
            {"$push": {"sequence": {"file_name": file_name, "file_id": file_id, "caption": caption}}},
            upsert=True
        )

    @staticmethod
    async def end_sequence(user_id):
        user = await user_col.find_one({"_id": user_id})
        files = user.get("sequence", [])
        await user_col.update_one({"_id": user_id}, {"$unset": {"sequence": ""}})
        return files

    @staticmethod
    async def cancel_sequence(user_id):
        await user_col.update_one(
            {"_id": user_id},
            {"$unset": {"sequence": ""}}
        )

    # === Premium ===

    @staticmethod
    async def add_user(user_id):
        user = await user_col.find_one({"_id": user_id})
        if not user:
            await user_col.insert_one({"_id": user_id})

    @staticmethod
    async def get_all_users():
        return [user["_id"] async for user in user_col.find({}, {"_id": 1})]

    @staticmethod
    async def check_premium(user_id):
        user = await user_col.find_one({"_id": user_id})
        if not user or "premium" not in user:
            return False
        expires = user["premium"]
        if datetime.utcnow() > expires:
            await user_col.update_one({"_id": user_id}, {"$unset": {"premium": 1}})
            return False
        return (expires - datetime.utcnow()).days

    @staticmethod
    async def add_premium(user_id, days):
        expires = datetime.utcnow() + timedelta(days=days)
        await user_col.update_one(
            {"_id": user_id},
            {"$set": {"premium": expires}},
            upsert=True
        )

    @staticmethod
    async def remove_premium(user_id):
        await user_col.update_one({"_id": user_id}, {"$unset": {"premium": 1}})

    @staticmethod
    async def list_premium_users():
        premium_users = user_col.find({"premium": {"$exists": True}})
        return [user["_id"] async for user in premium_users]
      
