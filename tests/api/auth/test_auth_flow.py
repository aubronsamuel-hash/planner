from backend.app.models.user import RefreshRequest, UserCreate, UserLogin
from backend.app.services import user_service


class TestAuthFlow:
    def setup_method(self) -> None:
        user_service.reset_state()

    def test_register_login_me_flow(self) -> None:
        created = user_service.create_user(UserCreate(email="alice@example.com", full_name="Alice", password="password123"))
        assert created.email == "alice@example.com"

        tokens = user_service.authenticate_user(UserLogin(email="alice@example.com", password="password123"))
        current = user_service.get_user_from_token(tokens.access_token)
        assert current is not None
        assert current.email == "alice@example.com"

    def test_refresh_invalid_token(self) -> None:
        request = RefreshRequest(refresh_token="invalid")
        try:
            user_service.refresh_tokens(request)
        except Exception as exc:  # noqa: BLE001
            assert "Invalid refresh token" in str(exc)
        else:  # pragma: no cover - defensive
            raise AssertionError("refresh should fail for invalid token")
