import pytest
from fastapi.testclient import TestClient

from main import app


def test_health_is_public() -> None:
    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_protected_accepts_correct_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("APP_API_KEY", "test-only-key")

    with TestClient(app) as client:
        response = client.get("/protected", headers={"X-API-Key": "test-only-key"})

    assert response.status_code == 200
    assert response.json() == {"message": "Access granted"}


def test_protected_rejects_wrong_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("APP_API_KEY", "test-only-key")

    with TestClient(app) as client:
        response = client.get("/protected", headers={"X-API-Key": "wrong-key"})

    assert response.status_code == 401
    assert response.json() == {"detail": "Missing or invalid API key"}


def test_protected_rejects_missing_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("APP_API_KEY", "test-only-key")

    with TestClient(app) as client:
        response = client.get("/protected")

    assert response.status_code == 401
    assert response.json() == {"detail": "Missing or invalid API key"}


def test_protected_requires_server_configuration(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("APP_API_KEY", raising=False)

    with TestClient(app) as client:
        response = client.get("/protected", headers={"X-API-Key": "test-only-key"})

    assert response.status_code == 503
    assert response.json() == {"detail": "API key is not configured"}
