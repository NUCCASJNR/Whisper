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
from anon.dependencies import JWTAuth

from .models import MainUser
from .schemas import (
    ActiveUsersSchema,
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


@api.post("/auth/signup/",
          response={
              201: MessageSchema,
              400: ErrorSchema
          })
def signup(request, payload: UserCreateSchema):
    """View for registering a new user

    :param request: Request object
    :param payload: User payload
    :param payload: UserCreateSchema:
    :returns: 201 or 400

    """
    username: str = payload.username
    if MainUser.custom_get(username=username):
        return 400, {
            "error": "Username already exists",
            "status": 400
        }
    payload_data = payload.dict()
    MainUser.custom_save(**payload_data)
    return 201, {"message": "Registration successful!",
                 "status": 201
                 }


@api.post('/auth/login/',
          response={
              200: LoginResponseSchema,
              400: ErrorSchema
          })
def user_login(request, payload: LoginSchema):
    """
    API view for logging in user
    :param request: Request object
    :param payload: LoginSchema
    :return: 200 if successful else 400
    """
    username = payload.username
    password = payload.password
    auth_user = authenticate(request, username=username, password=password)
    if auth_user is not None:
        login(request, auth_user)
        refresh = RefreshToken.for_user(auth_user)
        return 200, {
            "message": "Login Successful!",
            "access_token": str(refresh.access_token),
            "status": 200
        }
    return 400, {
        "error": "Invalid username or password",
        "status": 400
    }


@api.get('/active-users/',
         auth=JWTAuth(),
         response={
             200: ActiveUsersSchema,
             400: ErrorSchema
         })
def list_active_users(request):
    """
    API View for listing active users
    """
    users = MainUser.find_objs_by(**{"ready_to_chat": True})
    if users:
        exclude_user_id = str(request.user.id)
        user_ids = [
            str(user.id) for user in users if str(user.id) != exclude_user_id
        ]
        print(f'User Id: {user_ids}')
        u_list = []
        for user_id in user_ids:
            u_list.extend(user_id)
        print(f'User Id: {u_list}')
        return 200, {
            "message": "Active users Successfully Fetched",
            "user_ids": user_ids,
            "status": 200
        }
    return 400, {
        "error": "Oops, No active users at the moment,\
            Kindly check back later",
        "status": 400
    }
