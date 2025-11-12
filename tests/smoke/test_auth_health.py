from fastapi.testclient import TestClient

from backend.app.main import create_app
from backend.app.services import user_service


def test_smoke_login_flow() -> None:
    user_service.reset_state()
    client = TestClient(create_app())
    try:
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "smoke@example.com",
                "full_name": "Smoke",
                "password": "password123",
                "role": "admin",
            },
        )
        assert response.status_code == 201

        tokens = client.post(
            "/api/v1/auth/login",
            json={"email": "smoke@example.com", "password": "password123"},
        )
        assert tokens.status_code == 200
        assert tokens.json()["access_token"]
    finally:
        client.close()
