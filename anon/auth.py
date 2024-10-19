from ninja.security import HttpBearer
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from anon.models.token import BlacklistedToken
import json


class CustomJWTAuth(HttpBearer):
    def authenticate(self, request, token):
        try:
            access_token = request.headers.get("Authorization")
            if access_token and access_token.startswith("Bearer "):
                access_token = access_token.split("Bearer ")[1]
            else:
                access_token = None
            print(f'Request: {request.method}')
            if request.method == 'POST':
                try:
                    body = json.loads(request.body)
                    refresh_token = body.get('refresh_token')
                except (json.JSONDecodeError, TypeError):
                    refresh_token = None
            else:
                refresh_token = request.headers.get("Authorization")
                if refresh_token and refresh_token.startswith("Bearer "):
                    refresh_token = refresh_token.split("Bearer ")[1]
                else:
                    refresh_token = None
            access_found = BlacklistedToken.objects.filter(access_token=access_token).exists()
            refresh_found = BlacklistedToken.objects.filter(refresh_token=refresh_token).exists()

            if access_found or refresh_found:
                return None
            jwt_auth = JWTAuthentication()
            validated_token = jwt_auth.get_validated_token(token)
            user = jwt_auth.get_user(validated_token)
            return user

        except InvalidToken:
            return None
