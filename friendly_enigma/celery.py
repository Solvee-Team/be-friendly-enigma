from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from decouple import config

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'friendly_enigma.settings')
app = config('app')
# app.config_from_object('django.conf:settings', namespace='CELERY')
# app.autodiscover_tasks()
