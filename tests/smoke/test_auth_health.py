from backend.app.models.user import UserCreate, UserLogin
from backend.app.services import user_service


def test_smoke_login_flow() -> None:
    user_service.reset_state()
    user_service.create_user(UserCreate(email="smoke@example.com", full_name="Smoke", password="password123"))
    tokens = user_service.authenticate_user(UserLogin(email="smoke@example.com", password="password123"))
    assert tokens.access_token
