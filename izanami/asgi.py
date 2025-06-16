"""
ASGI config for izanami project.
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import challenges.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'izanami.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            challenges.routing.websocket_urlpatterns
        )
    ),
})
