from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.utils import timezone
from datetime import timedelta


class ExpiringTokenAuthentication(TokenAuthentication):
    expired_delta = timedelta(minutes=30)

    def authenticate_credentials(self, key):
        user, token = super().authenticate_credentials(key)
        if timezone.now() > token.created + self.expired_delta:
            token.delete()
            raise AuthenticationFailed("토큰 만료")
        return (user, token)
