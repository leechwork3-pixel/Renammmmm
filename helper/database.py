import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from config import Config


client = AsyncIOMotorClient(Config.DB_URL)
db = client[Config.DB_NAME]
user_col = db["users"]


class Element_Network:
    """
    MongoDB helper class to manage user data for AutoRenameBot.
    """

    @staticmethod
    async def set_format_template(user_id: int, template: str) -> None:
        """
        Save or update the rename format template for a user.
        """
        try:
            await user_col.update_one(
                {"_id": user_id},
                {"$set": {"template": template}},
                upsert=True,
            )
        except Exception as e:
            # Replace with your logging mechanism
            print(f"set_format_template error: {e}")

    @staticmethod
    async def get_format_template(user_id: int) -> Optional[str]:
        """
        Retrieve the rename format template for a user.
        """
        try:
            user = await user_col.find_one({"_id": user_id})
            return user.get("template") if user else None
        except Exception as e:
            print(f"get_format_template error: {e}")
            return None

    @staticmethod
    async def toggle_metadata(user_id: int) -> bool:
        """
        Toggle metadata embedding for a user; returns new status.
        """
        try:
            user = await user_col.find_one({"_id": user_id})
            current = user.get("metadata", False) if user else False
            new_status = not current
            await user_col.update_one(
                {"_id": user_id},
                {"$set": {"metadata": new_status}},
                upsert=True,
            )
            return new_status
        except Exception as e:
            print(f"toggle_metadata error: {e}")
            return False

    @staticmethod
    async def set_metadata(user_id: int, field: str, value: Any) -> None:
        """
        Set specific metadata field (e.g. title, author) for user.
        """
        try:
            await user_col.update_one(
                {"_id": user_id},
                {"$set": {f"meta.{field}": value}},
                upsert=True,
            )
        except Exception as e:
            print(f"set_metadata error: {e}")

    @staticmethod
    async def get_metadata(user_id: int) -> Dict[str, Any]:
        """
        Get all metadata for a user; returns empty dict if none set.
        """
        try:
            user = await user_col.find_one({"_id": user_id})
            return user.get("meta", {}) if user else {}
        except Exception as e:
            print(f"get_metadata error: {e}")
            return {}

    # === Sequence Mode ===

    @staticmethod
    async def start_sequence(user_id: int) -> None:
        """
        Initialize an empty sequence for the user.
        """
        try:
            await user_col.update_one(
                {"_id": user_id},
                {"$set": {"sequence": []}},
                upsert=True,
            )
        except Exception as e:
            print(f"start_sequence error: {e}")

    @staticmethod
    async def get_sequence(user_id: int) -> List[Dict[str, Any]]:
        """
        Return the user's current sequence list, empty if none.
        """
        try:
            user = await user_col.find_one({"_id": user_id})
            return user.get("sequence", []) if user else []
        except Exception as e:
            print(f"get_sequence error: {e}")
            return []

    @staticmethod
    async def store_sequence_file(
        user_id: int, file_name: str, file_id: str, caption: Optional[str] = None
    ) -> None:
        """
        Append a file to the user's sequence.
        """
        try:
            await user_col.update_one(
                {"_id": user_id},
                {"$push": {"sequence": {"file_name": file_name, "file_id": file_id, "caption": caption}}},
                upsert=True,
            )
        except Exception as e:
            print(f"store_sequence_file error: {e}")

    @staticmethod
    async def end_sequence(user_id: int) -> List[Dict[str, Any]]:
        """
        Retrieve the sequence files and clear the sequence.
        """
        try:
            user = await user_col.find_one({"_id": user_id})
            files = user.get("sequence", []) if user else []
            await user_col.update_one({"_id": user_id}, {"$unset": {"sequence": ""}})
            return files
        except Exception as e:
            print(f"end_sequence error: {e}")
            return []

    @staticmethod
    async def cancel_sequence(user_id: int) -> None:
        """
        Cancel sequence and remove any stored files.
        """
        try:
            await user_col.update_one({"_id": user_id}, {"$unset": {"sequence": ""}})
        except Exception as e:
            print(f"cancel_sequence error: {e}")

    # === Premium Handling ===

    @staticmethod
    async def add_user(user_id: int) -> None:
        """
        Add a new user if not present.
        """
        try:
            user = await user_col.find_one({"_id": user_id})
            if not user:
                await user_col.insert_one({"_id": user_id})
        except Exception as e:
            print(f"add_user error: {e}")

    @staticmethod
    async def get_all_users() -> List[int]:
        """
        List all user IDs.
        """
        try:
            return [user["_id"] async for user in user_col.find({}, {"_id": 1})]
        except Exception as e:
            print(f"get_all_users error: {e}")
            return []

    @staticmethod
    async def check_premium(user_id: int) -> int:
        """
        Return remaining premium days; 0 if none or expired.
        """
        try:
            user = await user_col.find_one({"_id": user_id})
            if not user or "premium" not in user:
                return 0
            expires: datetime = user["premium"]
            if datetime.utcnow() > expires:
                await user_col.update_one({"_id": user_id}, {"$unset": {"premium": 1}})
                return 0
            delta = expires - datetime.utcnow()
            return max(delta.days, 0)
        except Exception as e:
            print(f"check_premium error: {e}")
            return 0

    @staticmethod
    async def add_premium(user_id: int, days: int) -> None:
        """
        Add premium access days to a user.
        """
        try:
            expires = datetime.utcnow() + timedelta(days=days)
            await user_col.update_one(
                {"_id": user_id},
                {"$set": {"premium": expires}},
                upsert=True,
            )
        except Exception as e:
            print(f"add_premium error: {e}")

    @staticmethod
    async def remove_premium(user_id: int) -> None:
        """
        Remove premium access from user.
        """
        try:
            await user_col.update_one({"_id": user_id}, {"$unset": {"premium": 1}})
        except Exception as e:
            print(f"remove_premium error: {e}")

    @staticmethod
    async def list_premium_users() -> List[int]:
        """
        List user IDs with active premium status.
        """
        try:
            premium_users_cursor = user_col.find({"premium": {"$exists": True}})
            return [user["_id"] async for user in premium_users_cursor]
        except Exception as e:
            print(f"list_premium_users error: {e}")
            return []

