from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone

from phonenumber_field.modelfields import PhoneNumberField

from .fields import CompressedImageField

from .constants import CHAT_STYLES, THEMES


class User(AbstractBaseUser, PermissionsMixin):
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
    date_joined = models.DateTimeField(
        _("date joined"),
        default=timezone.now,
    )
    image = CompressedImageField(
        null=True, blank=True, default='cameraImg_NNGnCue.jpg')
    phone_number = PhoneNumberField(
        unique=True,
        blank=False,
        null=True
    )
    last_visit = models.DateTimeField(_("last visit"), blank=True, null=True)
    chat_style = models.CharField(
        max_length=100, choices=CHAT_STYLES, null=True, blank=True
    )
    theme = models.CharField(
        max_length=100, choices=THEMES, null=True, blank=True
    )
    contacts = models.ManyToManyField("User", blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "phone_number"

    def __str__(self):
        return self.first_name


class TempUser(models.Model):
    first_name = models.CharField(
        max_length=30,
    )
    last_name = models.CharField(
        _("last name"),
        max_length=150,
    )
    email = models.EmailField(
        max_length=255,
        blank=False,
    )

    class Meta:
        verbose_name = "Temp user"
        verbose_name_plural = "Temp users"
