from django.urls import re_path

from .consumers import MessageConsumer

websocket_urlpatterns = [
    re_path(
        r"ws/chat/(?P<sender_id>[\w-]+)/(?P<receiver_id>[\w-]+)/$",
        MessageConsumer.as_asgi(),
    ),
]
