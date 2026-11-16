import os
from html import escape
from time import time

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from starlette.middleware.sessions import SessionMiddleware

from saml_helpers import get_saml

app = FastAPI()
app.add_middleware(
    SessionMiddleware,
    secret_key=os.environ["SESSION_SECRET"],
    session_cookie="saml_demo",
    max_age=3600,
    same_site="lax",
)

pending_logins: dict[str, float] = {}


@app.get("/", response_class=HTMLResponse)
def home():
    return '<h1>SAML Login Demo</h1><a href="/login">Login with Keycloak</a>'


@app.get("/login")
async def login(request: Request):
    for key, expires in list(pending_logins.items()):
        if expires < time():
            del pending_logins[key]

    saml = await get_saml(request)
    login_url = saml.login()
    request_id = saml.get_last_request_id()
    pending_logins[request_id] = time() + 300
    request.session["request_id"] = request_id
    return RedirectResponse(login_url, status_code=303)


@app.post("/saml/acs")
async def callback(request: Request):
    request_id = request.session.pop("request_id", None)
    expires = pending_logins.pop(request_id, 0)
    if expires < time():
        raise HTTPException(400, "Login expired. Start again at /login.")

    saml = await get_saml(request)
    saml.process_response(request_id=request_id)
    if saml.get_errors() or not saml.is_authenticated():
        raise HTTPException(401, "SAML validation failed.")
    if saml.get_last_response_in_response_to() != request_id:
        raise HTTPException(401, "SAML response does not match this login.")

    request.session.clear()
    request.session["username"] = saml.get_nameid()
    return RedirectResponse("/profile", status_code=303)


@app.get("/profile", response_class=HTMLResponse)
def profile(request: Request):
    username = request.session.get("username")
    if not username:
        return RedirectResponse("/login", status_code=303)
    return f"<h1>Hello, {escape(username)}!</h1><p>You logged in using SAML.</p>"


@app.get("/saml/metadata")
async def metadata(request: Request):
    saml = await get_saml(request)
    xml = saml.get_settings().get_sp_metadata()
    return Response(xml, media_type="application/xml")
