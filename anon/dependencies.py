from typing import Optional

from ninja.security import HttpBearer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from jwt import decode, InvalidTokenError
from django.conf import settings


class JWTAuth(HttpBearer):
    def authenticate(self, request, token: str) -> Optional[dict]:
        try:
            validated_token = JWTAuthentication().get_validated_token(token)
            user = JWTAuthentication().get_user(validated_token)
            request.user = user
            return user
        except (InvalidToken, TokenError):
            return None


def get_user_from_token(auth_header):
    try:
        token = auth_header.split(' ')[1]
        decoded_data = decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return decoded_data['user_id']
    except (InvalidTokenError, IndexError, KeyError):
        return None
