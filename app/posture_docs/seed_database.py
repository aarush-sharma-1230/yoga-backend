"""
Seed yoga postures into MongoDB.

Postures are imported from all_postures (which combines and shuffles all
category modules). This file upserts them when the postures collection is empty.
"""

import asyncio
import os

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import UpdateOne

from app.posture_docs.all_postures import ALL_POSTURES

postures_data = ALL_POSTURES


async def seed_postures_if_empty() -> None:
    """
    Upsert all postures when the postures collection has no documents.

    Uses MONGO_URI and MONGO_DB_NAME from the environment. Skips when the
    collection is already populated.
    """

    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    database_name = os.getenv("MONGO_DB_NAME", "yoga")
    collection_name = "postures"

    client = AsyncIOMotorClient(mongo_uri, serverSelectionTimeoutMS=5000)

    try:
        await client.admin.command("ping")
        db = client[database_name]
        collection = db[collection_name]

        existing = await collection.find_one({}, projection={"_id": 1})
        if existing is not None:
            print("Skipping posture seed: postures collection is non-empty")
            return

        operations = [
            UpdateOne(
                {"client_id": posture["client_id"]},
                {"$set": posture},
                upsert=True,
            )
            for posture in postures_data
        ]

        if not operations:
            print("No posture documents to seed")
            return

        result = await collection.bulk_write(operations)
        print("Posture seeding complete")
        print(f"  upserted: {result.upserted_count}, modified: {result.modified_count}, total: {len(postures_data)}")
    finally:
        client.close()


if __name__ == "__main__":
    asyncio.run(seed_postures_if_empty())
