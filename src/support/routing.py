from django.urls import re_path
from support.consumers import ChatSupportConsumer

# Определяем WebSocket URL маршруты
websocket_urlpatterns = [
    re_path(r"ws/support/(?P<session_id>\w+)/$", ChatSupportConsumer.as_asgi()),
]
