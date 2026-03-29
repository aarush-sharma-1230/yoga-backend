"""
Prompt version selection. Set PROMPT_VERSION in .env or environment (v1–v4).
"""

import os

from dotenv import load_dotenv

load_dotenv()

VALID_VERSIONS = ("v1", "v2", "v3", "v4")
PROMPT_VERSION = os.getenv("PROMPT_VERSION", "v4").strip().lower()

if PROMPT_VERSION not in VALID_VERSIONS:
    raise ValueError(
        f"PROMPT_VERSION must be one of {VALID_VERSIONS}, got {PROMPT_VERSION!r}"
    )
