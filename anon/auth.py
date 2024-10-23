import json

from ninja.security import HttpBearer
import jwt
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
import logging
from anon.models.token import BlacklistedToken
from rest_framework.authentication import get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from django.utils.translation import gettext_lazy as _
from anon.models.user import MainUser

logger = logging.getLogger("apps")


class BaseTokenAuth:
    def get_user_from_token(self, token):
        try:
            # Decode the token using the secret key
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            logger.debug(f"Payload: {payload}")
            user_id = payload.get("user_id")
            if not user_id:
                logger.error(f"Token {token} is missing user_id.")
                return None
            # Retrieve the user from the database using the user ID
            try:
                user = MainUser.objects.get(id=user_id)
                logger.info(f"User {user.id} retrieved successfully from token.")
                return user
            except ObjectDoesNotExist:
                logger.error(f"No user found with ID {user_id}.")
                return None

        except jwt.ExpiredSignatureError:
            logger.warning(f"Token {token} has expired.")
            return None

        except jwt.InvalidTokenError as e:
            logger.error(f"Invalid token: {e}")
            return None

        return None


class CustomJWTAuth(HttpBearer, BaseTokenAuth):
    def authenticate(self, request, token):
        if not token:
            raise AuthenticationFailed(
                _("Invalid token header. No credentials provided.")
            )
        auth = get_authorization_header(request).split()
        logger.debug(f"Auth: {auth}")

        if not auth or auth[0].lower() != b"bearer":
            return None

        if len(auth) == 1:
            logger.debug("Invalid token header. No credentials provided.")
            raise AuthenticationFailed(
                _("Invalid token header. No credentials provided.")
            )

        if len(auth) > 2:
            logger.debug(
                "Invalid token header. Token string should not contain spaces."
            )
            raise AuthenticationFailed(
                _("Invalid token header. Token string should not contain spaces.")
            )

        token = auth[1].decode()
        logger.debug(f"Token received: {token}")
        try:
            body = json.loads(request.body)
            refresh_token = body.get("refresh_token")
        except (json.JSONDecodeError, TypeError):
            refresh_token = None
        try:
            BlacklistedToken.objects.get(access_token=token, refresh_token=refresh_token)
            logger.debug(f"Token {token} is blacklisted.")
            return None
        except BlacklistedToken.DoesNotExist:
            logger.debug(f"Token {token} is not blacklisted. Proceeding with authentication.")

        # Authenticate user based on token
        user = self.get_user_from_token(token)
        logger.info(f"LOgged User: {user}")
        if not user:
            logger.warning(f"Failed authentication: No user found for token {token}")
            return None

        logger.info(f"User {user.id} authenticated successfully with token {token}")
        return user


class AccessTokenAuth(HttpBearer):
    def authenticate(self, request, token):
        # Extract the token from the Authorization header
        if not token:
            raise AuthenticationFailed(
                _("Invalid token header. No credentials provided.")
            )
        auth = get_authorization_header(request).split()
        logger.debug(f"Auth: {auth}")

        if not auth or auth[0].lower() != b"bearer":
            return None

        if len(auth) == 1:
            logger.debug("Invalid token header. No credentials provided.")
            raise AuthenticationFailed(
                _("Invalid token header. No credentials provided.")
            )

        if len(auth) > 2:
            logger.debug(
                "Invalid token header. Token string should not contain spaces."
            )
            raise AuthenticationFailed(
                _("Invalid token header. Token string should not contain spaces.")
            )

        token = auth[1].decode()
        logger.debug(f"Token received: {token}")
        try:
            BlacklistedToken.objects.get(access_token=token)
            logger.debug(f"Token {token} is blacklisted.")
            return None
        except BlacklistedToken.DoesNotExist:
            logger.debug(f"Token {token} is not blacklisted. Proceeding with authentication.")

        # Authenticate user based on token
        user = self.get_user_from_token(token)
        logger.info(f"LOgged User: {user}")
        if not user:
            logger.warning(f"Failed authentication: No user found for token {token}")
            return None

        logger.info(f"User {user.id} authenticated successfully with token {token}")
        return user
