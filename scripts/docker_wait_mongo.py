"""Wait until MongoDB accepts connections (Docker entrypoint helper)."""

import asyncio
import os
import sys

from motor.motor_asyncio import AsyncIOMotorClient


async def wait_for_mongo() -> None:
    """Poll MongoDB until ping succeeds or timeout is reached."""

    uri = os.environ.get("MONGO_URI", "mongodb://mongo:27017")
    timeout_s = int(os.environ.get("MONGO_WAIT_TIMEOUT", "120"))

    for attempt in range(timeout_s):
        client: AsyncIOMotorClient | None = None
        try:
            client = AsyncIOMotorClient(uri, serverSelectionTimeoutMS=2000)
            await client.admin.command("ping")
            print(f"MongoDB reachable ({uri!r})")
            return
        except Exception as exc:
            print(f"Waiting for MongoDB ({attempt + 1}/{timeout_s})... {exc}")
            await asyncio.sleep(1)
        finally:
            if client is not None:
                client.close()

    print("Timed out waiting for MongoDB", file=sys.stderr)
    sys.exit(1)


def main() -> None:
    asyncio.run(wait_for_mongo())


if __name__ == "__main__":
    main()
