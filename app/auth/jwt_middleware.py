"""
JWT protection for routes via FastAPI dependencies.

Express-style middleware runs before a matched handler and mutates ``req``; in FastAPI,
the same pattern for *scoped* protection is a dependency injected with ``Depends()``:
it runs before the route handler, validates the token, and can attach data to the request.

Validated JWT claims are stored on ``request.state.user`` (Starlette’s equivalent of
attaching to the request object). Import ``jwt_access_payload`` and add
``jwt_payload: dict = Depends(jwt_access_payload)`` to protected endpoints.
"""

from typing import Any

from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials

from app.auth.auth_service import AuthService, security


async def jwt_access_payload(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict[str, Any]:
    """
    Require a valid Bearer access JWT; expose claims on ``request.state.user`` and return them.

    Raises ``AuthenticationError`` if the token is missing, malformed, or expired.
    """

    payload = AuthService.decode_access_token_payload(credentials.credentials)
    request.state.user = payload
    return payload
