from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from decouple import config

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'friendly_enigma.settings')
app = config('app')
