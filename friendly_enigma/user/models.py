# from django.contrib.auth.models import UserManager
from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        unique=True,
        max_length=255,
        blank=False,
    )

    first_name = models.CharField(
        _("first name"),
        max_length=30,
        blank=True,
    )
    last_name = models.CharField(
        _("last name"),
        max_length=150,
        blank=True,
    )
    date_of_birth = models.DateField(null=True)
    objects = CustomUserManager()
    USERNAME_FIELD = "email"
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into " "this admin site."),
    )
    is_superuser = models.BooleanField(
        _("superuser status"),
        default=False
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_("Designates whether this user should be treated as active."),
    )
    USERNAME_FIELD = "email"
    date_joined = models.DateTimeField(
        _("date joined"),
        default=timezone.now,
    )

    # @property
    # def is_staff(self):
    #     return self.is_staff
    #
    # @property
    # def is_superuser(self):
    #     return self.is_superuser
    #
    # @property
    # def is_active(self):
    #     return self.is_active
