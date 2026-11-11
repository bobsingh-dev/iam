# 🔐 Keycloak Login with FastAPI

A beginner Python project demonstrating OpenID Connect login.

## Features

- Keycloak-hosted login
- Authorization Code Flow with PKCE (S256)
- ID token validation through Authlib
- Protected page showing the username
- Signed application session cookie
- CSRF-protected logout and Keycloak logout

## Requirements

Python 3.12+ and Docker.

## Start Keycloak

```bash
docker run -d \
  --name keycloak-fastapi-simple \
  -p 127.0.0.1:8080:8080 \
  -e KC_BOOTSTRAP_ADMIN_USERNAME=admin \
  -e KC_BOOTSTRAP_ADMIN_PASSWORD=local-admin-password \
  quay.io/keycloak/keycloak:26.8.2 \
  start-dev
```

Wait for startup, then open http://localhost:8080/admin.

Admin login: `admin` / `local-admin-password`.

## Configure Keycloak

Create a realm named `simple`.

Create an OpenID Connect client:

| Setting | Value |
|---|---|
| Client ID | `python-app` |
| Client authentication | OFF |
| Standard flow | ON |
| Other authentication flows | OFF |
| PKCE method | S256 |
| Valid redirect URI | `http://localhost:8000/callback` |
| Valid post logout redirect URI | `http://localhost:8000/` |

Create user `bob`, filling in first name, last name, and email.
Set password to `local-demo-password`, with Temporary OFF.

## Run Python

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
export SESSION_SECRET="$(python -c 'import secrets; print(secrets.token_hex(32))')"
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Open http://localhost:8000 and log in as Bob.
Use localhost consistently so the callback URL matches.

## How it works

Keycloak authenticates the user and returns an authorization code.
Authlib exchanges the code using PKCE and validates the ID token.
FastAPI then creates a signed session containing the username.

The application never receives the user's password.
Passwords and tokens are not stored in its session cookie.

## Manual verification

1. Visit /profile while logged out: login is required.
2. Log in: the username appears.
3. Log out and confirm in Keycloak if prompted.
4. Revisit /profile: login is required again.

## Scope

Local learning demo using HTTP and development servers.
Login errors use default error responses.

The application cookie has a 30-minute inactivity limit and is
independent of the Keycloak session. Disabling a Keycloak user does
not immediately revoke an existing application cookie.

Production deployment requires HTTPS, Secure cookies, managed secrets,
and a session revocation strategy.

## Stop and restart

Stop Python with Ctrl+C.

```bash
docker stop keycloak-fastapi-simple
docker start keycloak-fastapi-simple
```

Keycloak configuration stays in the container. Removing the container
deletes its configuration because this demo uses no data volume.
EOF
