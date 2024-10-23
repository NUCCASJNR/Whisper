import json

from ninja.security import HttpBearer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from datetime import datetime
import jwt
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
import logging
from anon.models.token import BlacklistedToken
from rest_framework.authentication import get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from django.utils.translation import gettext_lazy as _
from anon.models.user import MainUser
from django.core.cache import cache
logger = logging.getLogger("apps")


class CustomJWTAuth(HttpBearer):
    def authenticate(self, request, token):
        try:
            mmm = cache.clear
            logger.info(f'Cache Result: {mmm}')
            access_token = request.headers.get("Authorization")
            if access_token and access_token.startswith("Bearer "):
                access_token = access_token.split("Bearer ")[1]
            else:
                access_token = None
            print(f"Request: {request.method}")
            if request.method == "POST":
                try:
                    body = json.loads(request.body)
                    refresh_token = body.get("refresh_token")
                except (json.JSONDecodeError, TypeError):
                    refresh_token = None
            else:
                refresh_token = request.headers.get("Authorization")
                if refresh_token and refresh_token.startswith("Bearer "):
                    refresh_token = refresh_token.split("Bearer ")[1]
                else:
                    refresh_token = None
            access_found = BlacklistedToken.objects.filter(
                access_token=access_token
            ).exists()
            refresh_found = BlacklistedToken.objects.filter(
                refresh_token=refresh_token
            ).exists()

            if access_found or refresh_found:
                return None
            jwt_auth = JWTAuthentication()
            try:
                validated_token = jwt_auth.get_validated_token(token)
            except (InvalidToken, TokenError):
                return None

            if validated_token['exp'] < datetime.utcnow().timestamp():
                return None

            user = jwt_auth.get_user(validated_token)
            return user

        except InvalidToken:
            return None


class AccessTokenAuth(HttpBearer):
    def authenticate(self, request, token):
        # Extract the token from the Authorization header
        if not token:
            raise AuthenticationFailed(_('Invalid token header. No credentials provided.'))
        auth = get_authorization_header(request).split()
        logger.debug(f'Auth: {auth}')

        if not auth or auth[0].lower() != b'bearer':
            return None

        if len(auth) == 1:
            logger.debug("Invalid token header. No credentials provided.")
            raise AuthenticationFailed(_('Invalid token header. No credentials provided.'))

        if len(auth) > 2:
            logger.debug("Invalid token header. Token string should not contain spaces.")
            raise AuthenticationFailed(_('Invalid token header. Token string should not contain spaces.'))

        token = auth[1].decode()
        logger.debug(f"Token received: {token}")

        # Authenticate user based on token
        user = self.get_user_from_token(token)
        logger.info(f"LOgged User: {user}")
        if not user:
            logger.warning(f"Failed authentication: No user found for token {token}")
            raise AuthenticationFailed(_('Invalid token. User not found.'))

        logger.info(f"User {user.id} authenticated successfully with token {token}")
        return user

    def get_user_from_token(self, token):
        try:
            # Decode the token using the secret key
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            logger.debug(f'Payload: {payload}')

            # Extract user ID (or email) from the token payload
            user_id = payload.get("user_id")
            if not user_id:
                logger.error(f"Token {token} is missing user_id.")
                raise AuthenticationFailed(_('Token is invalid or missing user information.'))
            # Retrieve the user from the database using the user ID
            try:
                user = MainUser.objects.get(id=user_id)
                logger.info(f"User {user.id} retrieved successfully from token.")
                return user
            except ObjectDoesNotExist:
                logger.error(f"No user found with ID {user_id}.")
                raise AuthenticationFailed(_('User not found.'))

        except jwt.ExpiredSignatureError:
            logger.warning(f"Token {token} has expired.")
            raise AuthenticationFailed(_('Token has expired.'))

        except jwt.InvalidTokenError as e:
            logger.error(f"Invalid token: {e}")
            return f'Error: {str(e)}'

        return None
