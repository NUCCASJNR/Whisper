#!/usr/bin/env python3
"""Contains user related API endpoints"""
import logging
from typing import Optional

from django.contrib.auth import authenticate, login, logout
from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from ninja import NinjaAPI, Router
from rest_framework_simplejwt.tokens import RefreshToken

from .models import MainUser
from .schemas import (
    MessageSchema,
    UserCreateSchema,
    ErrorSchema,
    LoginSchema,
    LoginResponseSchema
)

logger = logging.getLogger("apps")
api = NinjaAPI(version="2.0.0")
router = Router()


@api.get('/',
         response={
             200: MessageSchema
         })
def home(request):
    return 200, {
        'message': 'Welcome here, doc here: https://documenter.getpostman.com/view/28289943/2sA3rzLYfH',
        'status': 200
    }
