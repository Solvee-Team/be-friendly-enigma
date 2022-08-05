from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'friendly_enigma.settings')
app = Celery('friendly_enigma', broker='amqp://guest:guest@127.0.0.1:5672/')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
