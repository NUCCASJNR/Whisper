from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken

from anon.models.token import BlacklistedToken


class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        try:
            access_token = self.get_raw_token(request.headers.get("Authorization"))
            raw_token = self.get_raw_token(request.data.get("refresh_token"))
            access_found = BlacklistedToken.objects.filter(
                access_token=access_token
            ).exists()
            print(f"Access found: {access_found}")
            refresh_found = BlacklistedToken.objects.filter(
                refresh_token=raw_token
            ).exists()
            if access_found or refresh_found:
                raise InvalidToken("This token has been blacklisted.")
            return super().authenticate(request)
        except InvalidToken:
            raise InvalidToken("Invalid or blacklisted token")
