from django.urls import re_path 
 
from chat.consumers import ChatConsumer 

 # this file was used for routing websocket url,but now the url has been written with some modifications directly in NoWaste.asgi.py
websocket_urlpatterns = [
    re_path(r'chat/room/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),
]