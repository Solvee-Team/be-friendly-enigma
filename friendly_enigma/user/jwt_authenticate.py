from django.utils.timezone import now

from .models import User

from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.authentication import JWTAuthentication


class JWTAuthenticate(JWTAuthentication):

    def authenticate(self, request):
        result = super().authenticate(request)
        return result
