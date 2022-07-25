"""
ASGI config for turningpoint project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack
from chat import urls
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "friendly_enigma.settings")
# os.environ.setdefault("DJANGO_CONFIGURATION", "Local")


application = get_asgi_application()

application = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        # "websocket": URLRouter(urls.websocket_urlpatterns),
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(
                URLRouter(urls.websocket_urlpatterns)
            )
        )
    }
)
