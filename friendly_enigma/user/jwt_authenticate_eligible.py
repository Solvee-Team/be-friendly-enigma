from django.utils.timezone import now

from .models import User

from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.authentication import JWTAuthentication
# from auth_app import constants


class JWTAuthenticateEligible(JWTAuthentication):
    """
    Customized JWTAuthentication service from Rest Framework SimpleJWT class
    to handle user account activity and eligibility on each call
    """

    def authenticate(self, request):
        result = super().authenticate(request)
        return result
