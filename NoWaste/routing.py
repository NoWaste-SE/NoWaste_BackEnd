from django.urls import re_path 
 
from chat.consumers import ChatConsumer 
 
websocket_urlpatterns = [
    re_path(r'chat/room/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),
]