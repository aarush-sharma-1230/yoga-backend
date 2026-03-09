from motor.motor_asyncio import AsyncIOMotorDatabase
from app.auth.auth_interfaces import CreateUser, GetUserData
from bson import ObjectId
from app.globals.constants import pydantic_mongo_helper_projection


class AuthService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db

    async def create_user(self, user: CreateUser):
        user_obj = user.model_dump()
        result = await self.db["users"].insert_one(user_obj)

        return {"status": True, "user_id": str(result.inserted_id)}

    async def get_user_data(self, user_data: GetUserData):
        user_obj = await self.db["users"].find_one(
            {"_id": ObjectId(user_data.user_id)}, {**pydantic_mongo_helper_projection, "full_name": 1, "email": 1}
        )
        return {"status": True, "user": user_obj}
