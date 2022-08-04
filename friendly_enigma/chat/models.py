from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from model_utils.models import (
    TimeStampedModel,
    SoftDeletableModel,
)
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth import get_user_model
from typing import Optional, Any

UserModel: AbstractBaseUser = get_user_model()


class Dialog(TimeStampedModel):
    id = models.BigAutoField(primary_key=True, verbose_name=_("Id"))
    name = models.TextField(verbose_name=_("Name"), blank=True)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="dialogs")

    class Meta:
        verbose_name = _("Dialog")
        verbose_name_plural = _("Dialogs")

    def __str__(self):
        return f"Dialog {self.pk} - {self.users.count()} users"

    def list_users(self):
        return ", ".join([p.email for p in self.users.all()])

    def messages_count(self):
        return self.messages.count()

    @staticmethod
    def dialog_exists(u1: AbstractBaseUser, u2: AbstractBaseUser) -> Optional[Any]:
        return Dialog.objects.filter(users=u1).filter(users=u2).first()

    @staticmethod
    def create_if_not_exists(u1: AbstractBaseUser, u2: AbstractBaseUser):
        res = Dialog.dialog_exists(u1, u2)
        if not res:
            res = Dialog(name="Dialog")
            res.save()
            res.users.add(u1)
            res.users.add(u2)
        return res

    @staticmethod
    def get_dialogs_for_user(user: AbstractBaseUser):
        return Dialog.objects.filter(users=user).values_list("id", "users__pk")


class Message(TimeStampedModel, SoftDeletableModel):
    id = models.BigAutoField(primary_key=True, verbose_name=_("Id"))
    dialog = models.ForeignKey(
        Dialog, on_delete=models.CASCADE, related_name="messages", blank=True
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_("Author"),
        related_name="from_user",
        db_index=True,
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_("Recipient"),
        related_name="to_user",
        db_index=True,
    )
    text = models.TextField(verbose_name=_("Text"), blank=True)

    is_read = models.BooleanField(verbose_name=_("Is Read"), default=False)
    all_objects = models.Manager()

    @staticmethod
    def get_unread_count_for_dialog_with_user(dialog, recipient):
        return Message.objects.filter(
            dialog=dialog, recipient=recipient, is_read=False
        ).count()

    @staticmethod
    def get_unread_count_for_user(recipient):
        return Message.objects.filter(recipient=recipient, is_read=False).count()

    @staticmethod
    def get_last_message_for_dialog(dialog):
        return (
            Message.objects.filter(dialog=dialog)
            .select_related("sender", "recipient")
            .first()
        )

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        self.dialog = Dialog.create_if_not_exists(self.sender, self.recipient)
        super(Message, self).save(*args, **kwargs)

    class Meta:
        ordering = ("-created",)
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")
