import imp
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from jsonfield.fields import JSONField
from .choices import VERBS, TYPES

from django.contrib.contenttypes.fields import GenericForeignKey


class NotificationQuerySet(models.query.QuerySet):
    """Notification QuerySet"""

    def unsent(self, recipient):
        return self.filter(is_sent=False, recipient=recipient)

    def sent(self, recipient):
        return self.filter(is_sent=True, recipient=recipient)

    def unread(self, recipient):
        """Return only unread items in the current queryset"""
        return self.filter(is_read=False, recipient=recipient)

    def read(self, recipient):
        """Return only read items in the current queryset"""
        return self.filter(is_read=True, recipient=recipient)

    def mark_all_as_read(self, recipient):
        qset = self.unread(recipient)
        return qset.update(is_read=True)

    def mark_all_as_unread(self, recipient):
        qset = self.read(recipient)
        return qset.update(is_read=False)

    def mark_as_unsent(self, recipient):
        qset = self.sent(recipient)
        return qset.update(is_sent=False)

    def mark_as_sent(self, recipient):
        qset = self.unsent(recipient)
        return qset.update(is_sent=True)

    def unread_count(self, recipient):
        return self.unread(recipient).count()


class Notification(models.Model):

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=False,
        related_name="notifications",
        on_delete=models.CASCADE,
    )
    is_read = models.BooleanField(default=False, blank=False, db_index=True)

    limit = (
        models.Q(app_label="chat", model="message")
    )
    actor_content_type = models.ForeignKey(
        ContentType,
        related_name="notify_actor",
        on_delete=models.CASCADE,
        limit_choices_to=limit,
    )
    actor_object_id = models.CharField(max_length=255)
    actor = GenericForeignKey("actor_content_type", "actor_object_id")

    verb = models.CharField(max_length=50, choices=VERBS)
    text = models.CharField(max_length=255, blank=False)
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)
    is_sent = models.BooleanField(default=False, db_index=True)

    type = models.CharField(max_length=50, choices=TYPES, default=TYPES.Custom)

    data = JSONField(blank=True, null=True)
    objects = NotificationQuerySet.as_manager()

    class Meta:
        ordering = ("-timestamp",)
        index_together = ("recipient", "is_read")

    def __str__(self):
        ctx = {
            "actor": self.actor,
            "verb": self.verb,
            "timesince": self.timesince(),
        }
        return u"%(actor)s %(verb)s %(timesince)s ago" % ctx

    def timesince(self, now=None):
        """
        Shortcut for the ``django.utils.timesince.timesince`` function of the
        current timestamp.
        """
        from django.utils.timesince import timesince as timesince_

        return timesince_(self.timestamp, now)

    @property
    def slug(self):
        return self.id

    def mark_as_read(self):
        if not self.is_read:
            self.is_read = True
            self.save()

    def mark_as_unread(self):
        if self.is_read:
            self.is_read = False
            self.save()
