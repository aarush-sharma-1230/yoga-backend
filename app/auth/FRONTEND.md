# Web client contract (React)

## Login

1. Use [Google Identity Services](https://developers.google.com/identity/gsi/web) or `@react-oauth/google` to obtain a Google **ID token** (JWT).
2. `POST /auth/google` with JSON body `{ "id_token": "<token>" }` (no Bearer header required).
3. Read **`access_token`** from the JSON response and store it in **`localStorage`** (or your chosen store for the access JWT).
4. The response **`Set-Cookie`** header sets the **httpOnly** refresh cookie; path is configured by the server (default path prefix `/auth/refresh`). The browser will **not** send it on other routes.

## Authenticated API calls

- Send `Authorization: Bearer <access_token>` on every request that requires auth.
- Do **not** read or store the refresh token in JavaScript; it is **httpOnly**.

## Refresh (proactive and 401 retry)

- `POST /auth/refresh` with **`fetch(url, { method: "POST", credentials: "include" })`** so the refresh cookie is sent.
- On success, replace **`localStorage`** `access_token` with the new one from JSON.
- The server returns a new refresh via **`Set-Cookie`** (rotation); the old refresh is invalidated.

## CORS

- If the SPA and API share an origin (e.g. Nginx), `credentials: "include"` works with the same site. For cross-origin setups, the server must allow the front-end `Origin` and `Access-Control-Allow-Credentials: true` (already enabled in this app for CORS).

## Environment (backend)

Required: `JWT_SECRET`, `GOOGLE_CLIENT_ID` (Web client ID, used as ID token `aud`).

Optional: `ACCESS_TTL_MINUTES`, `REFRESH_TTL_DAYS`, `REFRESH_COOKIE_NAME`, `REFRESH_COOKIE_PATH`, `COOKIE_SECURE`, `COOKIE_SAMESITE`.
