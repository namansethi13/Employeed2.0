from django.urls import re_path
from .import consumers

websocker_urlpattersn = [
    re_path(r'ws/notify-socket/', consumers.NotifyConsumer.as_asgi())
]