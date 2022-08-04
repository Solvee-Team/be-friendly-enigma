from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics


from .models import User
from .serializers import UserSerializer, UserUpdatePasswordSerializer


class MyUserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = get_object_or_404(User, pk=request.user.pk)
        serializer = UserSerializer(
            user, context={"request": request}
        )
        return Response(serializer.data)

    def put(self, request):
        user = get_object_or_404(User, pk=request.user.pk)
        serializer = UserSerializer(
            user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class UserUpdatePasswordView(generics.UpdateAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = UserUpdatePasswordSerializer
    http_method_names = ["put"]

    def get_object(self):
        return self.request.user

    def put(self, request, *args, **kwargs):
        super().put(request, *args, **kwargs)
        return Response({"status": "ok", "message": _("Password changed.")})
