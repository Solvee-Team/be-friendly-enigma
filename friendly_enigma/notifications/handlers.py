from datetime import date, timedelta
import dateutil.parser
import logging
import json

from django.db.models.signals import post_save
from django.contrib.auth.models import Group
from django.db.models.query import QuerySet
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django_celery_beat.models import ClockedSchedule, PeriodicTask
from firebase_admin.messaging import (
    Message as FCMMessage,
    Notification as FCMNotification,
)
from fcm_django.models import FCMDevice

from user.models import User

from .choices import VERBS, TYPES, get_display_type
from chat.models import Message
from .models import Notification
from .signals import notify
from .serializers import NotificationSerializer


logger = logging.getLogger("notifications")


def new_message_handler(sender, instance, created, raw, using, update_fields, **kwargs):
    if created:
        task_name = f"New Message {instance.dialog.id}-{instance.recipient.id}"
        PeriodicTask.objects.filter(name=task_name).delete()
        today = timezone.now()
        next5Seconds = today + timedelta(seconds=5)
        clock5Seconds = ClockedSchedule.objects.create(clocked_time=next5Seconds)
        PeriodicTask.objects.create(
            clocked=clock5Seconds,
            one_off=True,
            name=task_name,
            task="jobs.tasks.send_new_message_notification",
            args=[instance.id],
        )


def notify_handler(verb, **kwargs):
    """
    Handler function to create Notification instance upon action signal call.
    """
    # Pull the options out of kwargs
    kwargs.pop("signal", None)
    recipient = kwargs.pop("recipient")
    actor = kwargs.pop("sender")
    text = kwargs.pop("text", "")
    title = kwargs.pop("title", "")
    type = kwargs.pop("type", TYPES.Custom)
    timestamp = kwargs.pop("timestamp", timezone.now())

    # Check if User or Group
    if isinstance(recipient, Group):
        recipients = recipient.user_set.all()
    elif isinstance(recipient, (QuerySet, list)):
        recipients = recipient
    else:
        recipients = [recipient]

    new_notifications = []

    noti_json = {}

    for recipient in recipients:
        newnotify = Notification(
            recipient=recipient,
            actor_content_type=ContentType.objects.get_for_model(actor)
            if actor != None
            else None,
            actor_object_id=actor.pk if actor != None else None,
            verb=str(verb),
            text=text,
            type=type,
            timestamp=timestamp,
        )

        if kwargs:
            newnotify.data = kwargs
        noti_json = NotificationSerializer(newnotify).data
        newnotify.save()
        new_notifications.append(newnotify)

    message_title = title or get_display_type(type)
    message = FCMMessage(
        notification=FCMNotification(title=message_title, body=text, image=""),
        data={"json": json.dumps(noti_json)},
    )
    devices = FCMDevice.objects.filter(user__in=recipients).all()
    devices.send_message(message)
    return new_notifications


post_save.connect(new_message_handler, sender=Message)
notify.connect(notify_handler, dispatch_uid="notifications.models.notification")
