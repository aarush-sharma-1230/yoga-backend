"""Run posture and theme seeds when collections are empty (Docker entrypoint)."""

import asyncio

from app.posture_docs.seed_database import seed_postures_if_empty
from app.themes.seed_themes import seed_themes_if_empty


async def run_seeds() -> None:
    await seed_themes_if_empty()
    await seed_postures_if_empty()


def main() -> None:
    asyncio.run(run_seeds())


if __name__ == "__main__":
    main()
