#!/usr/bin/env python3

"""User model for Whisper"""

from typing import Union

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser

from anon.models.base_model import BaseModel, models


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

    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=100)
    ready_to_chat = models.BooleanField(default=False)

    class Meta:
        db_table = "users"

    # Override the custom_save method
    @classmethod
    def custom_save(cls, **kwargs):
        """
        Overrides the custom_save method to hash the password before saving
        """
        if "password" in kwargs:
            kwargs["password"] = hash_password(kwargs["password"])
        return super().custom_save(**kwargs)
