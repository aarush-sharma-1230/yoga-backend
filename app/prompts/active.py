"""
Re-exports prompts from the active version (see version.py).
Import from here; no sys.modules or magic.
"""

import importlib

from app.prompts.version import PROMPT_VERSION

_base = f"app.prompts.{PROMPT_VERSION}"
_dev = importlib.import_module(f"{_base}.developer")
_user = importlib.import_module(f"{_base}.user")
_helpers = importlib.import_module(f"{_base}.helpers")

# Developer
ProfileContext = _dev.ProfileContext
extract_profile_context = _dev.extract_profile_context
get_sequence_composer_developer_prompt = _dev.get_sequence_composer_developer_prompt
get_summary_developer_prompt = _dev.get_summary_developer_prompt
get_yoga_coordinator_developer_prompt = _dev.get_yoga_coordinator_developer_prompt
get_request_reviewer_developer_prompt = _dev.get_request_reviewer_developer_prompt

# User
get_introduction_prompt = _user.get_introduction_prompt
get_transition_prompt = _user.get_transition_prompt
get_ending_prompt = _user.get_ending_prompt
get_sequence_user_prompt = _user.get_sequence_user_prompt
get_hard_priority_summary_prompt = _user.get_hard_priority_summary_prompt
get_medium_priority_summary_prompt = _user.get_medium_priority_summary_prompt
get_request_review_prompt = _user.get_request_review_prompt

# Helpers
duration_to_posture_range = _helpers.duration_to_posture_range
format_posture_catalogue = _helpers.format_posture_catalogue

__all__ = [
    "PROMPT_VERSION",
    "ProfileContext",
    "extract_profile_context",
    "get_sequence_composer_developer_prompt",
    "get_summary_developer_prompt",
    "get_yoga_coordinator_developer_prompt",
    "get_request_reviewer_developer_prompt",
    "get_introduction_prompt",
    "get_transition_prompt",
    "get_ending_prompt",
    "get_sequence_user_prompt",
    "get_hard_priority_summary_prompt",
    "get_medium_priority_summary_prompt",
    "get_request_review_prompt",
    "duration_to_posture_range",
    "format_posture_catalogue",
]
