from fastapi import Request
from onelogin.saml2.auth import OneLogin_Saml2_Auth

from saml_config import SAML_SETTINGS


async def get_saml(request: Request):
    form = await request.form() if request.method == "POST" else {}

    request_data = {
        "https": "off",
        "http_host": "localhost:8000",
        "server_port": "8000",
        "script_name": request.url.path,
        "get_data": dict(request.query_params),
        "post_data": dict(form),
    }

    return OneLogin_Saml2_Auth(request_data, SAML_SETTINGS)
