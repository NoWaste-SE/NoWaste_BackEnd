"""
ASGI config for NoWaste project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os
import django

from django.urls import re_path 
 

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "NoWaste.settings")

django.setup()

from django.core.asgi import get_asgi_application

application = get_asgi_application()

from chat.consumers import ChatConsumer
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator





application = ProtocolTypeRouter(
    {
        "http": application,
        "websocket": AllowedHostsOriginValidator(
             AuthMiddlewareStack(URLRouter([
                     re_path(r'ws/chat/room/(?P<room_name>.*)/$', ChatConsumer.as_asgi()),
                 ]))

        ),
    }
)
