from motor.motor_asyncio import AsyncIOMotorDatabase
from app.auth.auth_interfaces import CreateUser, GetUserData, UserProfilePayload
from bson import ObjectId
from app.globals.constants import pydantic_mongo_helper_projection
from app.prompts.profile_summaries import get_hard_priority_summary_prompt, get_medium_priority_summary_prompt


class AuthService:
    def __init__(self, db: AsyncIOMotorDatabase, yoga_agent=None):
        self.db = db
        self.yoga_agent = yoga_agent

    async def create_user(self, user: CreateUser):
        user_obj = user.model_dump()
        result = await self.db["users"].insert_one(user_obj)

        return {"status": True, "user_id": str(result.inserted_id)}

    async def get_user_data(self, user_data: GetUserData):
        user_obj = await self.db["users"].find_one(
            {"_id": ObjectId(user_data.user_id)}, {**pydantic_mongo_helper_projection, "full_name": 1, "email": 1}
        )
        return {"status": True, "user": user_obj}

    async def save_profile(self, user_id: str, profile: UserProfilePayload) -> dict:
        """Update user profile by user_id. Generates LLM summaries for Hard and Medium priority strategies and saves them."""
        profile_doc = profile.model_dump()

        if self.yoga_agent:
            hard_prompt = get_hard_priority_summary_prompt(profile_doc["hard_priority_strategy"])
            medium_prompt = get_medium_priority_summary_prompt(profile_doc["medium_priority_strategy"])
            hard_resp = self.yoga_agent.generate_text(prompt=hard_prompt)
            medium_resp = self.yoga_agent.generate_text(prompt=medium_prompt)
            profile_doc["hard_priority_summary"] = hard_resp["text"]
            profile_doc["medium_priority_summary"] = medium_resp["text"]

        await self.db["users"].update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"profile": profile_doc}},
        )
        return {"status": True}

    async def get_profile(self, user_id: str) -> dict:
        """Fetch user profile by user_id. Returns MongoDB document structure."""
        user = await self.db["users"].find_one({"_id": ObjectId(user_id)}, {"password": 0})
        if not user:
            raise RuntimeError("User not found")
        return user
