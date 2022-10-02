from .models import Message, Dialog, UserModel
from typing import Optional
import os
from django.db.models import Q
from rest_framework import serializers
from user.models import User
from django.contrib.auth import get_user_model
User = get_user_model()


class ChatUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["pk", "first_name", "last_name", "phone_number"]


class MessageSerializer(serializers.ModelSerializer):
    sender = ChatUserSerializer()
    recipient = ChatUserSerializer()
    is_outgoing = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = [
            "pk",
            "text",
            "created",
            "modified",
            "sender",
            "recipient",
            "is_outgoing",
            "is_read",
        ]

    def get_is_outgoing(self, obj):
        return self.context["user"] == obj.sender


class DialogsSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Dialog
        fields = ["user", "last_message", "unread_count"]

    def get_unread_count(self, obj):
        if "no_details" in self.context:
            return None
        return Message.get_unread_count_for_dialog_with_user(
            dialog=obj.pk, recipient=self.context["user"]
        )

    def get_last_message(self, obj):
        if "no_details" in self.context:
            return None
        last_message = Message.get_last_message_for_dialog(dialog=obj.pk)
        return (
            MessageSerializer(last_message, context=self.context).data
            if last_message
            else None
        )

    def get_user(self, obj):
        other = obj.users.exclude(pk=self.context["user"].id).first()
        return ChatUserSerializer(other, context=self.context).data if other else None


class ReadMessagesSerializer(serializers.Serializer):
    status = serializers.CharField(required=False)


class UnreadMessagesCountSerializer(serializers.Serializer):
    unread_count = serializers.IntegerField(required=True)
