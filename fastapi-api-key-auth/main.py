import os
from secrets import compare_digest
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import APIKeyHeader

app = FastAPI()
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def require_api_key(provided_key: Annotated[str | None, Depends(api_key_header)],) -> None:
    expected_key = os.getenv("APP_API_KEY")


    if not expected_key:
        raise HTTPException(status_code=503, detail="API key is not configured")

    if provided_key is None or not compare_digest(provided_key.encode(), expected_key.encode()):
        raise HTTPException(
                status_code=401,
                detail="Missing or invalid API key",
                headers={"WWW-Authenticate": "APIKey"},
                )



@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/protected", dependencies=[Depends(require_api_key)])
def protected() -> dict[str, str]:
    return {"message": "Access granted"}
