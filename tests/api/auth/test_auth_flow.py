from fastapi.testclient import TestClient

from backend.app.main import create_app
from backend.app.services import user_service


class TestAuthFlow:
    def setup_method(self) -> None:
        user_service.reset_state()
        self.client = TestClient(create_app())

    def teardown_method(self) -> None:
        self.client.close()

    def test_register_login_me_flow(self) -> None:
        register = self.client.post(
            "/api/v1/auth/register",
            json={
                "email": "alice@example.com",
                "full_name": "Alice",
                "password": "password123",
                "role": "admin",
            },
        )
        assert register.status_code == 201

        login = self.client.post(
            "/api/v1/auth/login",
            json={"email": "alice@example.com", "password": "password123"},
        )
        assert login.status_code == 200
        tokens = login.json()
        assert tokens["access_token"]

        current = self.client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {tokens['access_token']}"},
        )
        assert current.status_code == 200
        assert current.json()["email"] == "alice@example.com"

    def test_refresh_invalid_token(self) -> None:
        response = self.client.post(
            "/api/v1/auth/refresh", json={"refresh_token": "invalid"}
        )
        assert response.status_code == 401
