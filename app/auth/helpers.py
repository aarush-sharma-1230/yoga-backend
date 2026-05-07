"""Small HTTP helpers for auth (cookies)."""

from fastapi import Response
from typing import Any
from app.auth.settings import AuthSettings
from app.schemas.auth import USER_GOALS_FIELD, USER_GOALS_SUMMARY_FIELD, USER_MEDICAL_PROFILE_FIELD, USER_MEDICAL_PROFILE_SUMMARY_FIELD, UserGoals, UserMedicalProfile


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

def default_user_profile() -> dict[str, Any]:
    """
    Nested profile shape for new users: nested objects match persisted models; summaries are empty strings.

    Orchestration and prompts read ``user_medical_profile``, ``user_goals``,
    ``user_medical_profile_summary``, and ``user_goals_summary`` from the user document.
    """

    return {
        USER_MEDICAL_PROFILE_FIELD: UserMedicalProfile(
            medical_conditions=[],
            chronic_pain_areas=[],
            recent_surgery=None,
            user_notes=None,
        ).model_dump(),
        USER_GOALS_FIELD: UserGoals(
            experience_level=None,
            activity_level=None,
            primary_goal=[],
            user_notes=None,
        ).model_dump(),
        USER_MEDICAL_PROFILE_SUMMARY_FIELD: "",
        USER_GOALS_SUMMARY_FIELD: "",
    }
