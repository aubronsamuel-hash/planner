"""Pydantic user models used by the in-memory store."""
from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, Field, field_validator


class UserBase(BaseModel):
    email: str = Field(..., min_length=3)
    full_name: str = Field(..., min_length=1)
    role: str = Field(..., min_length=1)

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        if "@" not in value:
            raise ValueError("email must contain @")
        return value.lower()


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    email: str
    password: str


class UserRead(UserBase):
    id: int
    is_active: bool = True


class UserInDB(UserBase):
    id: int
    hashed_password: str
    is_active: bool = True
    created_at: datetime


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    refresh_token: str


__all__ = [
    "UserBase",
    "UserCreate",
    "UserRead",
    "UserInDB",
    "UserLogin",
    "TokenPair",
    "RefreshRequest",
]
