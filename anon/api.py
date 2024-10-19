#!/usr/bin/env python3
"""Contains user related API endpoints"""
import logging
from typing import Optional

from django.contrib.auth import authenticate, login, logout
from django.core.cache import cache
from django.http import JsonResponse
from anon.models.token import BlacklistedToken
from ninja import NinjaAPI, Router
from rest_framework_simplejwt.tokens import RefreshToken
from anon.dependencies import JWTAuth
from anon.auth import CustomJWTAuth


from .models import MainUser
from .schemas import (
    ActiveUsersSchema,
    ErrorSchema,
    LoginSchema,
    LogoutSchema,
    LoginResponseSchema,
    MessageSchema,
    PermissionSchema,
    StatusSchema,
    UserCreateSchema
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
        logger.info(f'token: {refresh}')
        return 200, {
            "message": "Login Successful!",
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
            "status": 200
        }
    return 400, {
        "error": "Invalid username or password",
        "status": 400
    }


@api.get('/active-users/',
         auth=CustomJWTAuth(),
         response={
             200: ActiveUsersSchema,
             400: ErrorSchema
         })
def list_active_users(request):
    """
    API View for listing active users
    """
    users = MainUser.objects.filter(ready_to_chat=True)
    logger.info(f'Active users fetched: {users}')
    if users.exists():
        exclude_user_id = str(request.user.id)
        user_ids = [
            str(user.id) for user in users if str(user.id) != exclude_user_id
        ]

        logger.info(f'User IDs: {user_ids}')
        return 200, {
            "message": "Active users successfully fetched",
            "user_ids": user_ids,
            "status": 200
        }
    return 400, {
        "error": "Oops, no active users at the moment, kindly check back later",
        "status": 400
    }


@api.post('/status/',
          auth=CustomJWTAuth(),
          response={
              200: MessageSchema,
              400: ErrorSchema
          })
def set_status(request, payload: StatusSchema):
    """
    API request for setting user ready_to_chat status
    """
    user = request.user
    option = payload.option

    try:
        updated = MainUser.custom_update(
            filter_kwargs={'username': user.username},
            update_kwargs={'ready_to_chat': option}
        )

        if updated:
            return 200, {
                'message': 'Ready to Chat status successfully updated',
                'status': 200
            }
        else:
            return 400, {
                'error': 'Failed to update Ready to Chat status. User not found.',
                'status': 400
            }

    except Exception as e:
        logger.error(f'Error updating Ready to Chat status for user {user.username}: {e}')
        return 400, {
            'error': 'An error occurred while updating the status. Please try again later.',
            'status': 400
        }


@api.post('/auth/logout/',
          auth=CustomJWTAuth(),
          response={
              200: MessageSchema,
              400: ErrorSchema,
              403: PermissionSchema,
              500: ErrorSchema
          })
def logout_user(request, payload: LogoutSchema):
    refresh_token = payload.refresh_token
    access_token = request.headers.get("Authorization")
    if access_token and access_token.startswith("Bearer "):
        access_token = access_token.split("Bearer ")[1]
    else:
        access_token = None

    if not refresh_token:
        return 400, {
            "error": "Refresh token is required.",
            "status": 400
        }
    try:
        token = RefreshToken(refresh_token)
        BlacklistedToken.objects.create(refresh_token=str(token), access_token=str(access_token))
        return 200, {
            "message": "Logged out successfully.",
            "status": 200
        }

    except Exception as e:
        return 500, {
            "error": str(e),
            "status": 500
        }
