from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from config import Config

# MongoDB connection
client = AsyncIOMotorClient(Config.DB_URL)
db = client[Config.DB_NAME]
user_col = db["users"]

class Element_Network:
    """
    MongoDB helper class to manage all user data for AutoRenameBot.
    """

    # ========== Ban System ==========
    @staticmethod
    async def ban_user(user_id: int):
        await user_col.update_one({"_id": user_id}, {"$set": {"banned": True}}, upsert=True)

    @staticmethod
    async def unban_user(user_id: int):
        await user_col.update_one({"_id": user_id}, {"$unset": {"banned": ""}})
        await user_col.update_one({"_id": user_id}, {"$unset": {"nsfw_strikes": ""}})

    @staticmethod
    async def is_banned(user_id: int) -> bool:
        user = await user_col.find_one({"_id": user_id})
        return user.get("banned", False) if user else False

    @staticmethod
    async def get_banned_users() -> List[int]:
        return [u["_id"] async for u in user_col.find({"banned": True})]

    # ========== NSFW Strikes ==========
    @staticmethod
    async def record_nsfw_strike(user_id: int) -> int:
        doc = await user_col.find_one({"_id": user_id}) or {}
        strikes = doc.get("nsfw_strikes", 0) + 1
        await user_col.update_one({"_id": user_id}, {"$set": {"nsfw_strikes": strikes}}, upsert=True)
        return strikes

    @staticmethod
    async def reset_strikes(user_id: int):
        await user_col.update_one({"_id": user_id}, {"$unset": {"nsfw_strikes": ""}})

    # ========== Queue System ==========
    @staticmethod
    async def add_to_queue(user_id: int, file_info: dict):
        await user_col.update_one({"_id": user_id}, {"$push": {"queue": file_info}}, upsert=True)

    @staticmethod
    async def get_queue(user_id: int):
        u = await user_col.find_one({"_id": user_id})
        return u.get("queue", [])

    @staticmethod
    async def clear_queue(user_id: int):
        await user_col.update_one({"_id": user_id}, {"$set": {"queue": []}})

    @staticmethod
    async def remove_from_queue(user_id: int, file_name: str):
        await user_col.update_one({"_id": user_id}, {"$pull": {"queue": {"file_name": file_name}}})

    @staticmethod
    async def clear_all_user_queues():
        await user_col.update_many({}, {"$unset": {"queue": ""}})

    # ========== Rename Format ==========
    @staticmethod
    async def set_format_template(user_id: int, template: str) -> None:
        await user_col.update_one({"_id": user_id}, {"$set": {"format_template": template}}, upsert=True)

    @staticmethod
    async def get_format_template(user_id: int) -> Optional[str]:
        user = await user_col.find_one({"_id": user_id})
        return user.get("format_template") if user else None

    # ========== Metadata ==========
    @staticmethod
    async def toggle_metadata(user_id: int) -> bool:
        user = await user_col.find_one({"_id": user_id})
        current = user.get("metadata_enabled", False) if user else False
        new_status = not current
        await user_col.update_one({"_id": user_id}, {"$set": {"metadata_enabled": new_status}}, upsert=True)
        return new_status

    @staticmethod
    async def set_metadata(user_id: int, field: str, value: Any) -> None:
        await user_col.update_one({"_id": user_id}, {"$set": {f"metadata.{field}": value}}, upsert=True)

    @staticmethod
    async def get_metadata(user_id: int) -> Dict[str, Any]:
        user = await user_col.find_one({"_id": user_id})
        return user.get("metadata", {}) if user else {}

    # ========== Sequence Mode ==========
    @staticmethod
    async def start_sequence(user_id: int) -> None:
        await user_col.update_one({"_id": user_id}, {"$set": {"sequence": []}}, upsert=True)

    @staticmethod
    async def get_sequence(user_id: int) -> List[Dict[str, Any]]:
        user = await user_col.find_one({"_id": user_id})
        return user.get("sequence", []) if user else []

    @staticmethod
    async def store_sequence_file(user_id: int, file_name: str, file_id: str, caption: Optional[str] = None) -> None:
        await user_col.update_one(
            {"_id": user_id},
            {"$push": {"sequence": {"file_name": file_name, "file_id": file_id, "caption": caption}}},
            upsert=True,
        )

    @staticmethod
    async def end_sequence(user_id: int) -> List[Dict[str, Any]]:
        user = await user_col.find_one({"_id": user_id})
        files = user.get("sequence", []) if user else []
        await user_col.update_one({"_id": user_id}, {"$unset": {"sequence": ""}})
        return files

    @staticmethod
    async def cancel_sequence(user_id: int) -> None:
        await user_col.update_one({"_id": user_id}, {"$unset": {"sequence": ""}})

    # ========== User Management ==========
    @staticmethod
    async def add_user(user_id: int) -> None:
        if not await user_col.find_one({"_id": user_id}):
            await user_col.insert_one({"_id": user_id})

    @staticmethod
    async def get_all_users() -> List[int]:
        return [u["_id"] async for u in user_col.find({}, {"_id": 1})]

    # ========== Premium Handling ==========
    @staticmethod
    async def check_premium(user_id: int) -> int:
        user = await user_col.find_one({"_id": user_id})
        if not user or "premium" not in user:
            return 0
        expires: datetime = user["premium"]
        if datetime.utcnow() > expires:
            await user_col.update_one({"_id": user_id}, {"$unset": {"premium": 1}})
            return 0
        delta = expires - datetime.utcnow()
        return max(delta.days, 0)

    @staticmethod
    async def add_premium(user_id: int, days: int) -> None:
        expires = datetime.utcnow() + timedelta(days=days)
        await user_col.update_one({"_id": user_id}, {"$set": {"premium": expires}}, upsert=True)

    @staticmethod
    async def remove_premium(user_id: int) -> None:
        await user_col.update_one({"_id": user_id}, {"$unset": {"premium": 1}})

    @staticmethod
    async def list_premium_users() -> List[int]:
        premium_users_cursor = user_col.find({"premium": {"$exists": True}})
        return [u["_id"] async for u in premium_users_cursor]

    # ========== Caption & Thumbnail ==========
    @staticmethod
    async def get_caption(user_id: int) -> str:
        user = await user_col.find_one({"_id": user_id})
        return user.get("caption", "")

    @staticmethod
    async def get_thumbnail(user_id: int) -> Optional[str]:
        user = await user_col.find_one({"_id": user_id})
        return user.get("thumbnail", None)
        
