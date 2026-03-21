"""Seed themes into MongoDB."""

import asyncio
import os

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import UpdateOne

from app.themes.themes_data import THEMES

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("MONGO_DB_NAME", "yoga")
COLLECTION_NAME = "themes"


async def seed_themes():
    client = AsyncIOMotorClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    try:
        await client.admin.command("ping")
        db = client[DATABASE_NAME]
        collection = db[COLLECTION_NAME]

        operations = [
            UpdateOne(
                {"slug": t["slug"]},
                {"$set": t},
                upsert=True,
            )
            for t in THEMES
        ]

        result = await collection.bulk_write(operations)
        print(f"Themes seeded: {result.upserted_count} inserted, {result.modified_count} updated")
    finally:
        client.close()


if __name__ == "__main__":
    asyncio.run(seed_themes())
