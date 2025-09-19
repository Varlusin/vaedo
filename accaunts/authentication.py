from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework import exceptions
from django.utils.translation import gettext_lazy as _


class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # Check if the token is in the cookies
        raw_token = request.COOKIES.get('access_token')
        if not raw_token:
            return None

        try:
            validated_token = UntypedToken(raw_token)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return self.get_user(validated_token), validated_token