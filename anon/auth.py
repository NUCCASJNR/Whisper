from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from anon.models.token import BlacklistedToken


class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        try:
            raw_token = self.get_raw_token(request.headers.get('Authorization'))
            if raw_token and BlacklistedToken.objects.filter(token=raw_token).exists():
                raise InvalidToken("This token has been blacklisted.")
            return super().authenticate(request)
        except InvalidToken:
            raise InvalidToken("Invalid or blacklisted token")
