from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'friendly_enigma.settings')
app = Celery('friendly_enigma', broker='amqp://guest:guest@127.0.0.1:5672/')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
# from configurations import importer
#
# from celery import Celery
#
# from django.conf import settings
#
# app = Celery("friendly_enigma")
#
# # Using a string here means the worker will not have to
# # pickle the object when using Windows.
# importer.install()
# app.config_from_object("django.conf:settings", "friendly_enigma.settings")
#
# # app.autodiscover_tasks(["jobs"])
#
# app.autodiscover_tasks(["chat"])
# app.conf.timezone = "UTC"
# app.conf.beat_scheduler = "django_celery_bea1t.schedulers:DatabaseScheduler"
