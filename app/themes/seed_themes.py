"""Seed themes into MongoDB."""

import asyncio
import os

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import UpdateOne

from app.themes.themes_data import THEMES


async def seed_themes_if_empty() -> None:
    """
    Upsert all themes when the themes collection has no documents.

    Uses MONGO_URI and MONGO_DB_NAME from the environment. Skips when the
    collection is already populated.
    """

    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    database_name = os.getenv("MONGO_DB_NAME", "yoga")
    collection_name = "themes"

    client = AsyncIOMotorClient(mongo_uri, serverSelectionTimeoutMS=5000)
    try:
        await client.admin.command("ping")
        db = client[database_name]
        collection = db[collection_name]

        existing = await collection.find_one({}, projection={"_id": 1})
        if existing is not None:
            print("Skipping themes seed: themes collection is non-empty")
            return

        operations = [
            UpdateOne(
                {"slug": t["slug"]},
                {"$set": t},
                upsert=True,
            )
            for t in THEMES
        ]

        if not operations:
            print("No theme documents to seed")
            return

        result = await collection.bulk_write(operations)
        print(f"Themes seeded: {result.upserted_count} inserted, {result.modified_count} updated")
    finally:
        client.close()


if __name__ == "__main__":
    asyncio.run(seed_themes_if_empty())
