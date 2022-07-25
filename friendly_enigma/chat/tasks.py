# from datetime import datetime, timedelta
from __future__ import absolute_import, unicode_literals
from celery import shared_task
# from firebase_admin.messaging import Message, Notification
#
# from user.models import User
# from notifications.signals import notify
# from notifications.choices import VERBS, TYPES
# from turningpoint.celery import app


# def send_new_message_notification(messageId):
#     from chat.models import Message
#
#     message = Message.objects.filter(id=messageId).first()
#     if not message.is_read:
#         notify.send(
#             sender=message,
#             recipient=message.recipient,
#             verb=VERBS.create,
#             type=TYPES.Message,
#             text=f"{message.sender.full_name}: {message.text}",
#         )
#     return True
