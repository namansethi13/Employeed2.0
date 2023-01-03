from django.urls import re_path
from .import consumers

websocker_urlpattersn = [
    re_path(r'ws/test-socket/', consumers.TestSubmission.as_asgi())
]