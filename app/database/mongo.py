from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
import os


class MongoDB:
  __instance = None

  def __new__(cls):
    if cls.__instance is None:
      print("Connecting to database...")
      cls.__instance = super(MongoDB, cls).__new__(cls)
      cls.__instance.client = AsyncIOMotorClient(os.getenv("MONGO_URI", "mongodb://localhost:27017"))
      cls.__instance.db = cls.__instance.client[os.getenv("MONGO_DB_NAME", "yoga")]
      print("Database connected")

    return cls.__instance

  def get_database(self) -> AsyncIOMotorDatabase:
    return self.db
