"""End-to-end tests for the authentication API."""
from __future__ import annotations

import hashlib
from datetime import datetime, timedelta, timezone

import pytest
from sqlalchemy import select

from backend.app.db.models import RefreshToken, User
from backend.app.db.session import get_session_maker


@pytest.mark.asyncio
async def test_full_auth_flow(client):
    register_payload = {
        "email": "demo@example.com",
        "full_name": "Demo User",
        "password": "SuperSecret!1",
        "role": "admin",
    }
    response = await client.post("/api/v1/auth/register", json=register_payload)
    assert response.status_code == 201

    login_response = await client.post(
        "/api/v1/auth/login",
        json={"email": "demo@example.com", "password": "SuperSecret!1"},
    )
    assert login_response.status_code == 200
    tokens = login_response.json()

    me_response = await client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {tokens['access_token']}"},
    )
    assert me_response.status_code == 200
    assert me_response.json()["email"] == "demo@example.com"

    refresh_response = await client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": tokens["refresh_token"]},
    )
    assert refresh_response.status_code == 200
    rotated = refresh_response.json()

    # Old access tokens are revoked once a refresh occurs.
    stale_me = await client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {tokens['access_token']}"},
    )
    assert stale_me.status_code == 401

    refreshed_me = await client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {rotated['access_token']}"},
    )
    assert refreshed_me.status_code == 200

    logout_response = await client.post(
        "/api/v1/auth/logout",
        json={"refresh_token": rotated["refresh_token"]},
        headers={"Authorization": f"Bearer {rotated['access_token']}"},
    )
    assert logout_response.status_code == 200

    post_logout_me = await client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {rotated['access_token']}"},
    )
    assert post_logout_me.status_code == 401

    post_logout_refresh = await client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": rotated["refresh_token"]},
    )
    assert post_logout_refresh.status_code == 401


@pytest.mark.asyncio
async def test_refresh_expired_token_returns_401(client):
    register_payload = {
        "email": "expiry@example.com",
        "full_name": "Expiry User",
        "password": "ExpiredSecret!1",
        "role": "admin",
    }
    response = await client.post("/api/v1/auth/register", json=register_payload)
    assert response.status_code == 201

    login_response = await client.post(
        "/api/v1/auth/login",
        json={"email": "expiry@example.com", "password": "ExpiredSecret!1"},
    )
    tokens = login_response.json()
    refresh_token = tokens["refresh_token"]

    refresh_hash = hashlib.sha256(refresh_token.encode("utf-8")).hexdigest()
    session_maker = get_session_maker()
    async with session_maker() as session:
        result = await session.execute(
            select(RefreshToken).where(RefreshToken.token_hash == refresh_hash)
        )
        record = result.scalar_one()
        record.expires_at = datetime.now(timezone.utc) - timedelta(minutes=1)
        await session.commit()

    expired_response = await client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": refresh_token},
    )
    assert expired_response.status_code == 401


@pytest.mark.asyncio
async def test_inactive_user_forbidden(client):
    register_payload = {
        "email": "inactive@example.com",
        "full_name": "Inactive User",
        "password": "InactiveSecret!1",
        "role": "admin",
    }
    response = await client.post("/api/v1/auth/register", json=register_payload)
    assert response.status_code == 201

    session_maker = get_session_maker()
    async with session_maker() as session:
        result = await session.execute(select(User).where(User.email == "inactive@example.com"))
        user = result.scalar_one()
        user.is_active = False
        await session.commit()

    login_attempt = await client.post(
        "/api/v1/auth/login",
        json={"email": "inactive@example.com", "password": "InactiveSecret!1"},
    )
    assert login_attempt.status_code == 403
