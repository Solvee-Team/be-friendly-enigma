from django.urls import re_path
from . import consumers
from . import views

websocket_urlpatterns = [
    re_path(r"^chat_ws$", consumers.ChatConsumer.as_asgi()),
]
