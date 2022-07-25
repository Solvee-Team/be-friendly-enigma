"""
ASGI config for friendly_enigma project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

from chat import urls
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import os
import django

# os.environ.setdefault("DJANGO_CONFIGURATION", "Local")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "friendly_enigma.settings")
django.setup()


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'friendly_enigma.settings')

application = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": application,
        "websocket": URLRouter(urls.websocket_urlpatterns),
    }
)
