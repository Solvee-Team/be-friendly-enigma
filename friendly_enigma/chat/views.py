from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.pagination import CursorPagination, PageNumberPagination
from rest_framework import generics, status, filters
from rest_framework.response import Response
from django_filters.rest_framework import (
    DjangoFilterBackend,
    FilterSet,
    ChoiceFilter,
    DateTimeFilter,
)
from django.shortcuts import render
from .models import Message, Dialog
from .serializers import (
    ChatUserSerializer,
    DialogsSerializer,
    MessageSerializer,
    ReadMessagesSerializer,
    UnreadMessagesCountSerializer,
)
from user.models import User
from django.db.models import Q
from django.db.models import Count
import logging
from django.contrib.auth import get_user_model
User = get_user_model()

logger = logging.getLogger("chat.consumers")


def index(request):
    return render(request, "chat/base.html")


class CursorSetPagination(CursorPagination):
    page_size = 100
    page_size_query_param = "page_size"
    cursor_query_param = "cursor"
    ordering = "-created"


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10000
    page_size_query_param = "page_size"
    max_page_size = 10000


class MessageFilter(FilterSet):
    from_time = DateTimeFilter(field_name="created", lookup_expr="gt")

    class Meta:
        model = Message
        fields = []


class MessageList(generics.ListAPIView):
    """
    Get Chat Messages for authenticated user
    """

    permission_classes = [IsAuthenticated]
    pagination_class = CursorSetPagination
    serializer_class = MessageSerializer
    filterset_class = MessageFilter

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["user"] = self.request.user
        return context

    def get_queryset(self):
        user = self.request.user

        if self.kwargs.get("user_id"):
            dialog = Dialog.dialog_exists(user, self.kwargs.get("user_id"))
            qs = Message.objects.filter(dialog=dialog).select_related(
                "sender", "recipient"
            )
        else:
            dialogs = Dialog.objects.filter(users=user)
            qs = Message.objects.filter(dialog__in=dialogs).prefetch_related(
                "sender", "recipient"
            )

        return qs.order_by("-created")


class DialogList(generics.ListAPIView):
    """
    Get Chat Dialogs for authenticated user (1-1 chat with other users)
    """

    permission_classes = [IsAuthenticated]
    pagination_class = CursorSetPagination
    serializer_class = DialogsSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["user"] = self.request.user
        return context

    def get_queryset(self):
        qs = (
            Dialog.objects.annotate(c=Count("users"))
            .filter(users=self.request.user)
            .filter(c__gt=1)
        )
        return qs.order_by("-created")


class UsersForMessagesList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        users = User.objects.all()
        serializer = ChatUserSerializer(users, many=True)
        return Response(serializer.data)


class ReadMessagesView(generics.RetrieveAPIView):
    """
    Mark Chat Messages (from a specific user ) as Read
    """

    permission_classes = [IsAuthenticated]
    serializer_class = ReadMessagesSerializer

    def get(self, request, *args, **kwargs):
        qs = Message.objects.filter(
            Q(recipient=self.request.user, sender=self.kwargs.get("user_id"))
        ).update(is_read=True)
        response = {
            "status": "success",
        }
        serializer = ReadMessagesSerializer(response)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UnreadMessagesCountView(generics.RetrieveAPIView):
    """
    Get unread messages count of authenticated user
    """

    permission_classes = [IsAuthenticated]
    serializer_class = UnreadMessagesCountSerializer

    def get(self, request, *args, **kwargs):
        response = {
            "unread_count": Message.get_unread_count_for_user(self.request.user),
        }
        serializer = UnreadMessagesCountSerializer(response)
        return Response(serializer.data, status=status.HTTP_200_OK)
