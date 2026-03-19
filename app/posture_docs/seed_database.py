"""
Seed yoga postures into MongoDB.

Postures are imported from all_postures (which combines and shuffles all
category modules). This file upserts them into the database.
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import UpdateOne

from app.posture_docs.all_postures import ALL_POSTURES

postures_data = ALL_POSTURES


async def seed_database():
    """
    Connects to MongoDB using Motor (async) and upserts the yoga postures.
    Upsert ensures idempotent execution.
    """
    # --- MONGODB CONFIGURATION ---
    MONGO_URI = "mongodb://localhost:27017/"
    DATABASE_NAME = "yoga"
    COLLECTION_NAME = "postures"

    client = AsyncIOMotorClient(MONGO_URI, serverSelectionTimeoutMS=5000)

    try:
        # Verify connection
        await client.admin.command("ping")
        print(f"✅ Successfully connected to MongoDB at {MONGO_URI}")

        db = client[DATABASE_NAME]
        collection = db[COLLECTION_NAME]

        # Prepare bulk operations
        operations = [
            UpdateOne(
                {"client_id": posture["client_id"]},
                {"$set": posture},
                upsert=True,
            )
            for posture in postures_data
        ]

        if operations:
            result = await collection.bulk_write(operations)
            print(f"✅ Database Seeding Complete!")
            print(f"   - Documents inserted/upserted: {result.upserted_count}")
            print(f"   - Documents modified: {result.modified_count}")
            print(f"   - Total postures processed: {len(postures_data)}")
            print("\nNote: Request the next batch of postures to continue populating the database.")

    except Exception as e:
        print(f"❌ An error occurred: {e}")
    finally:
        client.close()


if __name__ == "__main__":
    asyncio.run(seed_database())
