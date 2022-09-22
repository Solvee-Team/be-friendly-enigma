from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate
import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import status

from .models import User
from .serializers import (
    UserSerializer, UserUpdatePasswordSerializer,
    TokenRefreshSerializer, UpdateChatStyleSerializer,
    UpdateThemeSerializer
)


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


class UserSearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        phone_number = self.request.query_params.get('phone_number')
        phone_number = phone_number.replace(" ", "+")
        queryset = User.objects.all()
        if phone_number:
            queryset = queryset.filter(phone_number__icontains=phone_number)
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)


class DecoratedTokenRefreshView(TokenRefreshView):
    serializer_class = TokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class DeleteAcount(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = User.objects.get(id=request.user.id)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UpdateChatStyle(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = UpdateChatStyleSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UpdateTheme(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)
