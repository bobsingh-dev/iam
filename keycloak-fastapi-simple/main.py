import os

from html import escape
from secrets import compare_digest, token_urlsafe
from urllib.parse import parse_qs, urlencode
from authlib.integrations.starlette_client import OAuth

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.middleware.sessions import SessionMiddleware


app = FastAPI()


app.add_middleware(
    SessionMiddleware,
    secret_key=os.environ["SESSION_SECRET"],
    max_age=1800,
    same_site="lax",
    https_only=False,  # local http only
)

ISSUER = "http://localhost:8080/realms/simple"

oauth = OAuth()
keycloak = oauth.register(
    name="keycloak",
    client_id="python-app",
    server_metadata_url=f"{ISSUER}/.well-known/openid-configuration",
    client_kwargs={
        "scope": "openid profile",
        "code_challenge_method": "S256",
        "token_endpoint_auth_method": "none",
    },
    timeout=10,
)


@app.get("/", response_class=HTMLResponse)
async def home():
    return '<h1>My Python App</h1><a href="/profile">Log in with Keycloak</a>'


@app.get("/login")
async def login(request: Request):
    return await keycloak.authorize_redirect(
        request, "http://localhost:8000/callback"
    )


@app.get("/callback")
async def callback(request: Request):
    # Authlib verifies the login response and validates the ID token.
    token = await keycloak.authorize_access_token(request)

    request.session.clear()
    request.session["username"] = token["userinfo"]["preferred_username"]
    request.session["csrf"] = token_urlsafe(32)

    return RedirectResponse("/profile", status_code=303)


@app.get("/profile", response_class=HTMLResponse)
async def profile(request: Request):
    if "username" not in request.session:
        return RedirectResponse("/login", status_code=303)

    username = escape(request.session["username"])
    csrf = escape(request.session["csrf"])

    return f"""
    <h1>Hello, {username}!</h1>
    <p>This page requires login.</p>
    <form action="/logout" method="post">
      <input type="hidden" name="csrf" value="{csrf}">
      <button>Log out</button>
    </form>
    """


@app.post("/logout")
async def logout(request: Request):
    body = (await request.body()).decode()
    provided = parse_qs(body).get("csrf", [""])[0]
    expected = request.session.get("csrf", "")

    if not expected or not compare_digest(expected, provided):
        raise HTTPException(status_code=403, detail="invalid logout request")

    request.session.clear()

    parameters = urlencode({
        "client_id": "python-app",
        "post_logout_redirect_uri": "http://localhost:8000/",
    })

    return RedirectResponse(
        f"{ISSUER}/protocol/openid-connect/logout?{parameters}",
        status_code=303,
    )

