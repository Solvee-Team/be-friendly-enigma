from django.utils import timezone
from drf_extra_fields.fields import Base64ImageField

from django.contrib.auth import password_validation
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.state import token_backend

from .models import User

from .constants import CHAT_STYLES, THEMES


class RegisterBaseInfoSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "phone_number",
            'password'
        ]

    def create(self, validated_data):
        user, created = User.objects.update_or_create(
            phone_number=validated_data.get("phone_number"),
            first_name=validated_data.get("first_name"),
            last_name=validated_data.get("last_name"),
            password=validated_data.get("password"),
            chat_style=CHAT_STYLES[1][1],
            theme=THEMES[1][1],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    last_visit = serializers.DateTimeField(format="%Y-%m-%dT%H:%M")

    class Meta:
        model = User
        fields = [
            "pk",
            "phone_number",
            "first_name",
            "last_name",
            "image",
            "last_visit",
            "chat_style",
            "theme",
        ]


class UserUpdatePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=64, write_only=True, required=True)
    new_password = serializers.CharField(max_length=64, write_only=True, required=True)
    new_password_confirmation = serializers.CharField(
        max_length=64, write_only=True, required=True
    )

    def validate_old_password(self, old_password):
        if self.instance.check_password(old_password):
            return old_password
        exc = ValidationError(_("Old password is incorrect"))
        raise exc

    def validate(self, data):
        if data.get("new_password") != data.get("new_password_confirmation"):
            exc = ValidationError(_("Passwords don't match."))
            raise exc
        password_validation.validate_password(data.get("new_password"), self.instance)
        return data

    def save(self):
        user = self.instance
        user.set_password(self.validated_data.get("new_password"))
        return user.save()


class TokenRefreshSerializer(TokenRefreshSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        decoded_payload = token_backend.decode(data["access"], verify=True)
        user = User.objects.filter(pk=decoded_payload['user_id']).update(last_visit=timezone.now())
        return data


class UpdateChatStyleSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["chat_style", "theme"]

        def update(self, instance, validated_data):
            new_chat_style = validated_data["chat_style"]
            user = User.objects.update(chat_style=new_chat_style)
            return user


class UpdateThemeSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["theme"]

        def update(self, validated_data):
            new_theme = validated_data["theme"]
            User.objects.update(theme=new_theme)


class AddContactSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=12, write_only=True, required=True)

    def update(self, instance, validated_data):
        user = self.context['request'].user
        phone_number = validated_data["phone_number"]
        added_contact = User.objects.get(phone_number=phone_number)
        user.contacts.add(added_contact)
        return UserSerializer(added_contact)
