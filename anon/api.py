#!/usr/bin/env python3
"""Contains user related API endpoints"""
import logging

from django.contrib.auth import authenticate, login
from ninja import NinjaAPI, Router
from rest_framework_simplejwt.tokens import RefreshToken

from anon.auth import AccessTokenAuth, CustomJWTAuth
from anon.models.token import BlacklistedToken
from anon.utils.generator import generate_websocket_url, set_user_pin

from anon.models.user import MainUser
from anon.models.message import Conversation
from anon.schemas import (
    ActiveUsersSchema,
    ConversationSchema,
    ErrorSchema,
    LoginResponseSchema,
    LoginSchema,
    LogoutSchema,
    MessageSchema,
    PermissionSchema,
    ProfileResponseSchema,
    StatusSchema,
    UpdateProfileSchema,
    UserCreateSchema,
    WhisperResponseSchema,
    WhisperSchema,
)

logger = logging.getLogger("apps")
api = NinjaAPI(version="2.0.0")
router = Router()


@api.get("/", response={200: MessageSchema})
def home(request):
    return 200, {
        "message": "Welcome here, doc here: https://documenter.getpostman.com/view/28289943/2sA3rzLYfH",
        "status": 200,
    }


@api.post("/auth/signup", response={201: MessageSchema, 400: ErrorSchema})
def signup(request, payload: UserCreateSchema):
    """View for registering a new user

    :param request: Request object
    :param payload: User payload
    :param payload: UserCreateSchema:
    :returns: 201 or 400

    """
    username: str = payload.username
    if MainUser.custom_get(username=username):
        return 400, {"error": "Username already exists", "status": 400}
    payload_data = payload.dict()
    MainUser.custom_save(**payload_data)
    return 201, {"message": "Registration successful!", "status": 201}


@api.post("/auth/login", response={200: LoginResponseSchema, 400: ErrorSchema})
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
        logger.info(f"token: {refresh}")
        return 200, {
            "message": "Login Successful!",
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
            "status": 200,
        }
    return 400, {"error": "Invalid username or password", "status": 400}


@api.get(
    "/active-users",
    auth=AccessTokenAuth(),
    response={200: ActiveUsersSchema, 400: ErrorSchema, 500: ErrorSchema},
)
def list_active_users(request):
    current_user = request.auth
    logger.info(f"Current User: {current_user}")

    if current_user is None:
        logger.error("Invalid or expired token, no current user.")
        return 400, {"error": "Invalid or expired token", "status": 400}

    try:
        users = MainUser.objects.filter(ready_to_chat=True)
        logger.info(f"Active users fetched: {users}")

        if users.exists():
            exclude_user_id = str(current_user.id)
            users_info = {
                str(user.id): {"user_id": str(user.id), "user_bio": user.bio}
                for user in users
                if str(user.id) != exclude_user_id
            }
            logger.info(f"User infos: {users_info}")

            return 200, {
                "message": "Active users successfully fetched",
                "bios": [info["user_bio"] for info in users_info.values()],
                "ids": [info["user_id"] for info in users_info.values()],
                "status": 200,
            }

        return 400, {
            "error": "Oops, no active users at the moment, kindly check back later",
            "status": 400,
        }

    except Exception as e:
        logger.error(f"Error fetching active users: {str(e)}")
        return 500, {"error": str(e), "status": 500}


@api.post(
    "/status", auth=AccessTokenAuth(), response={200: MessageSchema, 400: ErrorSchema}
)
def set_status(request, payload: StatusSchema):
    """
    API request for setting user ready_to_chat status
    """
    user = request.auth
    option = payload.option

    try:
        updated = MainUser.custom_update(
            filter_kwargs={"username": user.username},
            update_kwargs={"ready_to_chat": option},
        )

        if updated:
            return 200, {
                "message": "Ready to Chat status successfully updated",
                "status": 200,
            }
        else:
            return 400, {
                "error": "Failed to update Ready to Chat status. User not found.",
                "status": 400,
            }

    except Exception as e:
        logger.error(
            f"Error updating Ready to Chat status for user {user.username}: {e}"
        )
        return 400, {
            "error": "An error occurred while updating the status. Please try again later.",
            "status": 400,
        }


@api.post(
    "/auth/logout",
    auth=CustomJWTAuth(),
    response={
        200: MessageSchema,
        400: ErrorSchema,
        403: PermissionSchema,
        500: ErrorSchema,
    },
)
def logout_user(request, payload: LogoutSchema):
    refresh_token = payload.refresh_token
    access_token = request.headers.get("Authorization")
    if access_token and access_token.startswith("Bearer "):
        access_token = access_token.split("Bearer ")[1]
    else:
        access_token = None

    if not refresh_token:
        return 400, {"error": "Refresh token is required.", "status": 400}
    try:
        token = RefreshToken(refresh_token)
        BlacklistedToken.objects.create(
            refresh_token=str(token), access_token=str(access_token)
        )
        return 200, {"message": "Logged out successfully.", "status": 200}

    except Exception as e:
        return 500, {"error": str(e), "status": 500}


@api.get(
    "/profile",
    auth=AccessTokenAuth(),
    response={
        200: ProfileResponseSchema,
        400: ErrorSchema,
        404: ErrorSchema,
        500: ErrorSchema,
    },
)
def profile(request):
    """API view for displaying a user profile"""
    current_user = request.auth
    logger.info(f"{request.auth} | {request.user}")
    if current_user is None:
        return 400, {"error": "Invalid or expired token", "status": 400}
    logger.info(
        f"Request user: {current_user.id if current_user else 'No user authenticated'}"
    )

    if not current_user:
        return 400, {"error": "Invalid or expired token", "status": 400}

    try:
        user = MainUser.objects.get(id=current_user.id)
        if user:
            logger.info(f"User profile fetched successfully for user ID {user.id}")
            return 200, {
                "message": "User profile successfully fetched",
                "bio": user.bio,
                "username": user.username,
                "id": str(user.id),
                "ready_to_chat": user.ready_to_chat,
            }
        else:
            logger.warning(f"No user found with ID {current_user.id}")
            return 404, {"error": "No such user found", "status": 404}
    except Exception as e:
        logger.error(f"Error fetching profile for user {current_user.id}: {str(e)}")
        return 500, {"error": str(e), "status": 500}


@api.put(
    "/update-profile",
    auth=AccessTokenAuth(),
    response={
        200: MessageSchema,
        400: ErrorSchema,
        403: ErrorSchema,
        404: ErrorSchema,
        500: ErrorSchema,
    },
)
def update_profile(request, payload: UpdateProfileSchema):
    """
    API view for updating user profile
    """
    current_user = request.auth
    payload_data = payload.dict()
    if current_user is None:
        return 400, {"error": "Invalid or expired token", "status": 400}

    try:
        user = MainUser.objects.get(id=current_user.id)
        if user:
            logger.info(f"Payload Keys: {payload_data}")
            update_kwargs = {
                key: value for key, value in payload_data.items() if value is not None
            }
            if "username" in update_kwargs.keys():
                existing_user = MainUser.objects.filter(
                    username=update_kwargs.get("username")
                )
                if existing_user:
                    return 400, {"error": "User with username Exists", "status": 400}
                # Update the user with the filtered data
                MainUser.custom_update(
                    filter_kwargs={"id": current_user.id}, update_kwargs=update_kwargs
                )
                return 200, {"message": "Profile successfully updated.", "status": 200}
            else:
                MainUser.custom_update(
                    filter_kwargs={"id": current_user.id}, update_kwargs=update_kwargs
                )
                return 200, {"message": "Profile successfully updated.", "status": 200}
        else:
            return 404, {"error": "No such user found", "status": 404}
    except Exception as e:
        logger.error(f"Error updating user {current_user.id} Profile: {str(e)}")
        return 500, {"error": str(e), "status": 500}


@api.post(
    "/whisper",
    auth=AccessTokenAuth(),
    response={
        200: WhisperResponseSchema,
        400: ErrorSchema,
        500: ErrorSchema,
        403: ErrorSchema,
    },
)
def whisper(request, payload: WhisperSchema):
    """
    API View for initiating convo
    """
    current_user = request.auth
    if current_user is None:
        return 400, {"error": "Invalid or expired token", "status": 403}
    try:
        receiever = MainUser.custom_get(**{"id": payload.id})
        if receiever:
            url = generate_websocket_url(current_user.id, payload.id)
            return 200, {
                "message": "Convo successfully initialized",
                "url": url,
                "status": 200,
            }
        else:
            return 400, {"error": "User not found"}
    except Exception as e:
        return 500, {"error": str(e), "status": 500}


@api.get(
    "/conversations",
    auth=AccessTokenAuth(),
    response={
        200: ConversationSchema,
        400: ErrorSchema,
        500: ErrorSchema,
        403: ErrorSchema,
    },
)
def get_conversations(request):
    """
    API View for getting all conversations
    """
    current_user = request.auth
    if current_user is None:
        return 400, {"error": "Invalid or expired token", "status": 403}
    try:
        conversations = Conversation.objects.filter(participants=current_user)
        logger.info(f"Conversations: {conversations}")
        if conversations.exists():
            return 200, {
                "message": "Conversations successfully fetched",
                "conversations": [
                    {
                        "id": conversation.id,
                        "name": conversation.name,
                        "participants": [participant.username for participant in conversation.participants.all()],
                        "messages": [
                            {
                                "id": message.id,
                                "sender": message.sender.username,
                                "receiver": message.receiver.username,
                                "content": message.content,
                            }
                            for message in conversation.messages.all()
                        ],
                    }
                    for conversation in conversations
                ],
                "status": 200,
            }
        return 200, {
            "message": "No conversations found",
            "conversations": [],
            "status": 200,
        }
    except Exception as e:
        return 500, {"error": str(e), "status": 500}
