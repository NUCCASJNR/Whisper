#!/usr/bin/env python3
"""Contains user related schemas definition"""
from typing import Any, List, Optional

from ninja import Schema
from pydantic import BaseModel, model_validator


class UserSchema(Schema):
    """ """

    username: str


class UserCreateSchema(Schema):
    """ """

    username: str
    password: Any


class LoginSchema(BaseModel):
    username: str
    password: str

    @model_validator(mode="before")
    def check_email_or_username(cls, values):
        username = values.get("username")
        if not username:
            raise ValueError("Username must be provided")
        return values


class ErrorSchema(Schema):
    """ """

    error: str
    status: int


class MessageSchema(Schema):
    """Message schema"""

    message: str
    status: int


class LoginResponseSchema(Schema):
    """Login Response Schema"""

    message: str
    status: int
    access_token: str
    refresh_token: str


class ActiveUsersSchema(Schema):
    """Active users schema"""

    message: str
    status: int
    ids: List
    bios: List


class StatusSchema(Schema):
    """SChema for setting user status"""

    option: bool


class PermissionSchema(Schema):
    status: int
    error: str


class LogoutSchema(Schema):
    refresh_token: str


class ProfileSchema(Schema):
    """Schema for user profile
    Args:
        refresh_token ([type]): [description]
    """
    refresh_token: str


class ProfileResponseSchema(Schema):
    """Schema for user profile
    Args:
        Schema ([type]): [description]
        message ([type]): [description]
        bio ([type]): [description]
        username ([type]): [description]
        ready_to_chat ([type]): [description]
        id ([type]): [description
    """
    message: str
    bio: str
    username: str
    ready_to_chat: bool
    id: str


class UpdateProfileSchema(Schema):
    """Schema for updating user profile
    Args:
        Schema ([type]): [description]
        password ([type]): [description]
        username ([type]): [description]
        bio ([type]): [description]
    """
    password: Optional[Any] = None
    username: Optional[str] = None
    bio: Optional[str] = None


class WhisperSchema(Schema):
    """
    Schema for whisper
    Args:
        Schema ([type]): [description]
        id ([type]): [description]
    """
    id: str


class WhisperResponseSchema(Schema):
    """
    Schema for whisper response
    Args:
        Schema ([type]): [description]
        message ([type]): [description]
        url ([type]): [description]
        status ([type]): [description]
    """
    message: str
    url: str
    status: int


class ConversationSchema(Schema):
    """
    Schema for conversation
    Args:
        Schema ([type]): [description]
        message ([type]): [description]
        status ([type]): [description]
    """
    conversations: List
    status: int
