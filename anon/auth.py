from ninja.security import HttpBearer
from rest_framework_simplejwt.exceptions import InvalidToken
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
            if request.method == 'POST':
                try:
                    body = json.loads(request.body)
                    raw_token = body.get('refresh_token')
                except (json.JSONDecodeError, TypeError):
                    raw_token = None
            else:
                raw_token = request.GET.get('refresh_token')

            # Check if the tokens are blacklisted
            access_found = BlacklistedToken.objects.filter(access_token=access_token).exists()
            refresh_found = BlacklistedToken.objects.filter(refresh_token=raw_token).exists()

            if access_found or refresh_found:
                raise InvalidToken({"detail": "This token has been blacklisted.", "code": "token_not_valid"})
            
            # Call the parent method to complete authentication
            return super().authenticate(request, token)

        except InvalidToken as e:
            # Only catch and re-raise the exception with additional context if necessary
            raise InvalidToken({"detail": "Invalid or blacklisted token", "code": "token_not_valid"}) from e
