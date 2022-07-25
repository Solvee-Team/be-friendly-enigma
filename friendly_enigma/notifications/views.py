from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import CursorPagination, PageNumberPagination
from rest_framework import generics, status
from rest_framework.response import Response

from .models import Notification
from .serializers import (
    NotificationSerializer,
    UnreadNotificationCountSerializer,
    ReadNotificationSerializer,
)
import logging

logger = logging.getLogger("notifications")


class CursorSetPagination(CursorPagination):
    page_size = 100
    page_size_query_param = "page_size"
    cursor_query_param = "cursor"
    ordering = "-timestamp"


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = "page_size"
    max_page_size = 1000


class AllNotificationList(generics.ListAPIView):
    """
    Get all notifications
    """

    permission_classes = [IsAuthenticated]
    pagination_class = CursorSetPagination
    serializer_class = NotificationSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["user"] = self.request.user
        return context

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)


class UnreadNotificationList(generics.ListAPIView):
    """
    Get unread notifications
    """

    permission_classes = [IsAuthenticated]
    pagination_class = CursorSetPagination
    serializer_class = NotificationSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["user"] = self.request.user
        return context

    def get_queryset(self):
        return Notification.objects.unread(self.request.user)


class ReadNotificationsView(generics.RetrieveAPIView):
    """
    Mark Notifications as Read
    """

    permission_classes = [IsAuthenticated]
    serializer_class = ReadNotificationSerializer

    def get(self, request, *args, **kwargs):
        Notification.objects.filter(recipient=self.request.user).update(is_read=True)
        response = {
            "status": "success",
        }
        serializer = ReadNotificationSerializer(response)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UnreadNotificationsCountView(generics.RetrieveAPIView):
    """
    Get unread messages count of authenticated user
    """

    permission_classes = [IsAuthenticated]
    serializer_class = UnreadNotificationCountSerializer

    def get(self, request, *args, **kwargs):
        response = {
            "unread_count": Notification.objects.unread_count(self.request.user),
        }
        serializer = UnreadNotificationCountSerializer(response)
        return Response(serializer.data, status=status.HTTP_200_OK)
