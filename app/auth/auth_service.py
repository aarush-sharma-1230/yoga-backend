from motor.motor_asyncio import AsyncIOMotorDatabase

from app.auth.auth_interfaces import (
    CreateUser,
    GetUserData,
    HardPriorityStrategy,
    MediumPriorityStrategy,
)
from bson import ObjectId


class AuthService:
    def __init__(self, db: AsyncIOMotorDatabase, summary_agent=None):
        self.db = db
        self.summary_agent = summary_agent

    async def create_user(self, user: CreateUser):
        user_obj = user.model_dump()
        result = await self.db["users"].insert_one(user_obj)

        return {"status": True, "user_id": str(result.inserted_id)}

    async def get_user_data(self, user_data: GetUserData):
        payload = user_data.model_dump()
        user_obj = await self.db["users"].find_one(
            {"_id": ObjectId(payload["user_id"])},
            {"full_name": 1, "email": 1, "profile": 1},
        )
        return {"status": True, "user": user_obj}

    async def save_hard_priority_strategy(self, user_id: str, strategy: HardPriorityStrategy) -> dict:
        """Persist medical / safety strategy only. LLM hard summary runs in a background task."""
        doc = strategy.model_dump()
        await self.db["users"].update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"profile.hard_priority_strategy": doc}},
        )
        return {"status": True}

    async def save_medium_priority_strategy(self, user_id: str, strategy: MediumPriorityStrategy) -> dict:
        """Persist goals / experience strategy only. LLM medium summary runs in a background task."""
        doc = strategy.model_dump()
        await self.db["users"].update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"profile.medium_priority_strategy": doc}},
        )
        return {"status": True}

    async def generate_hard_summary_and_update_profile(self, user_id: str, hard_strategy: dict) -> None:
        """Background task: generate hard-priority summary only."""
        if not self.summary_agent:
            return
        hard_resp = await self.summary_agent.generate_summary(hard_strategy, "hard")
        await self.db["users"].update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"profile.hard_priority_summary": hard_resp["text"]}},
        )

    async def generate_medium_summary_and_update_profile(self, user_id: str, medium_strategy: dict) -> None:
        """Background task: generate medium-priority summary only."""
        if not self.summary_agent:
            return
        medium_resp = await self.summary_agent.generate_summary(medium_strategy, "medium")
        await self.db["users"].update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"profile.medium_priority_summary": medium_resp["text"]}},
        )

    async def get_profile(self, user_id: str) -> dict:
        """Fetch user profile by user_id. Returns MongoDB document structure."""
        user = await self.db["users"].find_one({"_id": ObjectId(user_id)}, {"password": 0})
        if not user:
            raise RuntimeError("User not found")
        return user
