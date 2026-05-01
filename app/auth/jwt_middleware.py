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

import jwt
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials

from app.auth.auth_service import AuthService, security


async def jwt_access_payload(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict[str, Any]:
    """
    Require a valid Bearer access JWT; expose claims on ``request.state.user`` and return them.

    Raises ``401`` if the token is missing, malformed, or expired.
    """

    try:
        payload = AuthService.decode_access_token_payload(credentials.credentials)
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed.",
        )
    request.state.user = payload
    return payload
