#!/usr/bin/env python3

"""User model for Whisper"""

from anon.models.base_model import BaseModel, models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
from typing import Union


def hash_password(password: Union[str, int]) -> str:
    """
    Hashes the password
    @param password: str | int
    @return: The hashed password
    """
    return make_password(password)


class MainUser(AbstractUser, BaseModel):
    """
    User model
    """

    username = models.TextField(max_length=50, unique=True)
    password = models.TextField(max_length=100)

    # Overide the custom_save nethod
    @classmethod
    def custom_save(cls, **kwargs):
        """
        Overrides the custom_save method to hash the password before saving
        """
        if "password" in kwargs:
            kwargs["password"] = hash_password(kwargs["password"])
        return super().custom_save(**kwargs)
