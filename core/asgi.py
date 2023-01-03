"""
ASGI config for core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import notify.routing
import tests.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')


application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket' : AuthMiddlewareStack(
        URLRouter([
            *notify.routing.websocker_urlpattersn,
            *tests.routing.websocker_urlpattersn,
        ])
    )
})