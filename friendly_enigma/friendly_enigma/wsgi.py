"""
WSGI config for friendly_enigma project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

from whitenoise import WhiteNoise
from configurations.wsgi import get_wsgi_application
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "friendly_enigma.settings")
os.environ.setdefault("DJANGO_CONFIGURATION", "Local")


# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'friendly_enigma.settings')

application = get_wsgi_application()
application = WhiteNoise(application)
