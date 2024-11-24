#!/usr/bin/env python3
"""Contains user related schemas definition"""
from typing import Any, List, Optional

from ninja import Schema, File, UploadedFile, Form
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
    users: List[dict]


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
    profile_picture: Optional[str]


class UpdateProfileSchema(Schema):
    """
    Schema for updating user profile.

    Args:
        password: User's password (optional).
        username: User's username (optional).
        bio: User's biography (optional).
        ready_to_chat: Status if user is ready to chat (optional).
        profile_picture: User's profile picture (optional).
    """

    password: Optional[str] = Form(None)
    username: Optional[str] = Form(None)
    bio: Optional[str] = Form(None)
    ready_to_chat: Optional[bool] = Form(None)
    profile_picture: Optional[UploadedFile] = File(None)


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
