import os
from django.db.models import Q
from rest_framework import serializers
from drf_yasg import openapi
from user.models import User
from chat.models import Dialog, Message
from chat.serializers import DialogsSerializer
from .models import Notification


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["pk", "first_name", "last_name", "full_name"]


class ActorFieldSerializer(serializers.RelatedField):
    class Meta:
        swagger_schema_fields = {
            "type": openapi.TYPE_OBJECT,
        }

    def to_representation(self, value):
        serializer = None
        if isinstance(value, User):
            serializer = UserSerializer(value)
        elif isinstance(value, Message):
            serializer = DialogsSerializer(
                value.dialog, context={"user": value.recipient, "no_details": True}
            )

        return serializer.data if serializer != None else None


class NotificationSerializer(serializers.ModelSerializer):
    actor = ActorFieldSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = [
            "pk",
            "is_read",
            "verb",
            "timestamp",
            "actor",
            "type",
            "text",
        ]


class ReadNotificationSerializer(serializers.Serializer):
    status = serializers.CharField(required=False)


class UnreadNotificationCountSerializer(serializers.Serializer):
    unread_count = serializers.IntegerField(required=True)
