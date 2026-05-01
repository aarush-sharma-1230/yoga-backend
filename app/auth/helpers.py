"""Small HTTP helpers for auth (cookies)."""

from fastapi import Response

from app.auth.settings import AuthSettings


def set_refresh_cookie(response: Response, refresh_token: str, settings: AuthSettings) -> None:
    """Attach rotated refresh token as an httpOnly cookie scoped to the refresh path."""

    max_age = settings.refresh_ttl_days * 24 * 60 * 60
    response.set_cookie(
        key=settings.refresh_cookie_name,
        value=refresh_token,
        max_age=max_age,
        path=settings.refresh_cookie_path,
        httponly=True,
        secure=settings.cookie_secure,
        samesite=settings.cookie_samesite,
    )


def clear_refresh_cookie(response: Response, settings: AuthSettings) -> None:
    """Clear the refresh cookie (e.g. on logout)."""

    response.delete_cookie(
        key=settings.refresh_cookie_name,
        path=settings.refresh_cookie_path,
        httponly=True,
        secure=settings.cookie_secure,
        samesite=settings.cookie_samesite,
    )
