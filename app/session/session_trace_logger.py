"""
Temporary trace logging for session generation flow. Remove this module and all
trace() calls when debugging is complete.
"""
from datetime import datetime
from zoneinfo import ZoneInfo

IST = ZoneInfo("Asia/Kolkata")


def trace(message: str, session_id: str | None = None) -> None:
    ts = datetime.now(IST).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    prefix = f"[{ts} IST]"
    if session_id:
        prefix += f" [session={session_id}]"
    print(f"{prefix} {message}")
