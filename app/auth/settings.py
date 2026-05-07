"""Environment-backed settings for JWT cookies and Google OIDC."""

import os
from dataclasses import dataclass
from functools import lru_cache


@dataclass(frozen=True)
class AuthSettings:
    """Authentication-related configuration loaded from the environment."""

    jwt_secret: str
    google_client_id: str
    access_ttl_minutes: int
    refresh_ttl_days: int
    refresh_cookie_name: str
    refresh_cookie_path: str
    cookie_secure: bool
    cookie_samesite: str
    user_daily_llm_usd_cap: float


def _parse_bool(raw: str | None) -> bool:
    if not raw: 
        return False

    return raw.strip().lower() == "true"


@lru_cache
def get_auth_settings() -> AuthSettings:
    """ Load auth settings once per process """

    jwt_secret = os.getenv("JWT_SECRET")
    google_client_id = os.getenv("GOOGLE_CLIENT_ID")
    access_ttl = int(os.getenv("ACCESS_TTL_MINUTES"))
    refresh_ttl_days = int(os.getenv("REFRESH_TTL_DAYS"))
    cookie_secure = _parse_bool(os.getenv("COOKIE_SECURE"), default=False)
    cookie_samesite = os.getenv("COOKIE_SAMESITE", "lax").lower()
    user_daily_llm_usd_cap = float(os.getenv("USER_DAILY_LLM_USD_CAP"))

    refresh_cookie_name = "y_refresh_token"
    refresh_cookie_path = "/auth/refresh"

    return AuthSettings(
        jwt_secret=jwt_secret.strip(),
        google_client_id=google_client_id.strip(),
        access_ttl_minutes=access_ttl,
        refresh_ttl_days=refresh_ttl_days,
        refresh_cookie_name=refresh_cookie_name,
        refresh_cookie_path=refresh_cookie_path,
        cookie_secure=cookie_secure,
        cookie_samesite=cookie_samesite,
        user_daily_llm_usd_cap=user_daily_llm_usd_cap,
    )
