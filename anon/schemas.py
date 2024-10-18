#!/usr/bin/env python3
"""Contains user related schemas definition"""
from typing import Optional
from ninja import Schema
from pydantic import BaseModel, EmailStr, root_validator, model_validator


class UserSchema(Schema):
    """ """

    username: str


class UserCreateSchema(Schema):
    """ """

    username: str
    password: str


class LoginSchema(BaseModel):
    username: str
    password: str

    @model_validator(mode='before')
    def check_email_or_username(cls, values):
        username = values.get('username')
        if not username:
            raise ValueError('Username must be provided')
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
