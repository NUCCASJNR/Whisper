import json

from ninja.security import HttpBearer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from datetime import datetime
import logging
from anon.models.token import BlacklistedToken
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
    def authenticate(self, request, token=None):
        # Clear any existing authentication data at the beginning of each request
        cache.clear()
        logger.info("Cache cleared.")
        request.auth = None
        request.user = None

        try:
            logger.info(f"Received Authorization header: {request.headers.get('Authorization')}")
            access_token = request.headers.get("Authorization")
            if not access_token or not access_token.startswith("Bearer "):
                logger.error("No Bearer token found or incorrect format.")
                return None

            token = access_token.split("Bearer ")[1].strip()
            logger.info(f"Extracted Token: {token}")

            # Check if token is blacklisted
            if BlacklistedToken.objects.filter(access_token=token).exists():
                logger.error("Token is blacklisted")
                return None

            jwt_auth = JWTAuthentication()
            try:
                validated_token = jwt_auth.get_validated_token(token)
                logger.info(f"Validated Token: {validated_token}")
            except (InvalidToken, TokenError) as e:
                logger.error(f"Token validation error: {e}")
                return None

            # Check token expiration
            if validated_token['exp'] < datetime.utcnow().timestamp():
                logger.error(f"Token has expired. Expiration: {validated_token['exp']}, Current Time: {datetime.utcnow().timestamp()}")
                return None

            # Get the user from the token
            user = jwt_auth.get_user(validated_token)
            logger.info(f"Authenticated User: {user}")
            request.auth = user  # Set the authenticated user to request.auth
            request.user = user   # Also set the user here
            return user
        except Exception as e:
            logger.error(f"Authentication failed: {e}")
            return None
