from drf_extra_fields.fields import Base64ImageField

from django.contrib.auth import password_validation
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import User


class RegisterBaseInfoSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            'password'
        ]

    def create(self, validated_data):
        user, created = User.objects.update_or_create(
            email=validated_data.get("email"),
            first_name=validated_data.get("first_name"),
            last_name=validated_data.get("last_name"),
            password=validated_data.get("password"),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False)

    class Meta:
        model = User
        fields = [
            "pk",
            "email",
            "first_name",
            "last_name",
            "image",
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
        logger.exception(exc)
        raise exc

    def validate(self, data):
        if data.get("new_password") != data.get("new_password_confirmation"):
            exc = ValidationError(_("Passwords don't match."))
            logger.exception(exc)
            raise exc
        password_validation.validate_password(data.get("new_password"), self.instance)
        return data

    def save(self):
        user = self.instance
        user.set_password(self.validated_data.get("new_password"))
        return user.save()
