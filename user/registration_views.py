from django.contrib.auth.base_user import BaseUserManager
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .models import User
from .serializers import (
    RegisterBaseInfoSerializer,
    UserSerializer,
)


class RegisterBaseInfoView(generics.CreateAPIView):
    serializer_class = RegisterBaseInfoSerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        user = RegisterBaseInfoSerializer(data=request.data)
        user.is_valid(raise_exception=True)
        user.save()
        return Response(
            UserSerializer(user.instance).data, status=status.HTTP_200_OK
        )
