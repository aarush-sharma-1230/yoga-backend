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


def _parse_bool(raw: str | None, default: bool) -> bool:
    if raw is None:
        return default
    return raw.strip().lower() in ("1", "true", "yes", "on")


@lru_cache
def get_auth_settings() -> AuthSettings:
    """
    Load auth settings once per process.

    Required: JWT_SECRET, GOOGLE_CLIENT_ID (OAuth 2.0 Web client ID used as ID token audience).
    """

    jwt_secret = os.getenv("JWT_SECRET")
    google_client_id = os.getenv("GOOGLE_CLIENT_ID")
    if not jwt_secret or not jwt_secret.strip():
        raise RuntimeError("JWT_SECRET environment variable is required for authentication")
    if not google_client_id or not google_client_id.strip():
        raise RuntimeError("GOOGLE_CLIENT_ID environment variable is required for Google sign-in")

    access_ttl = int(os.getenv("ACCESS_TTL_MINUTES", "15"))
    refresh_ttl_days = int(os.getenv("REFRESH_TTL_DAYS", "14"))
    refresh_cookie_name = os.getenv("REFRESH_COOKIE_NAME", "refresh_token")
    refresh_cookie_path = os.getenv("REFRESH_COOKIE_PATH", "/auth/refresh")
    cookie_secure = _parse_bool(os.getenv("COOKIE_SECURE"), default=False)
    cookie_samesite = os.getenv("COOKIE_SAMESITE", "lax").lower()
    if cookie_samesite not in ("lax", "strict", "none"):
        cookie_samesite = "lax"
    user_daily_llm_usd_cap = float(os.getenv("USER_DAILY_LLM_USD_CAP", "0.1"))

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
