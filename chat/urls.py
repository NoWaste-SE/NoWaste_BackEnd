# chat/urls.py
from django.urls import path

from django.urls import re_path 
 
from chat.consumers import ChatConsumer 

from django.urls.conf import include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from .views import *
# from .views import *


# urlpatterns = [
#     path("", views.index, name="index"),
#     #  path("chat_room/", views.room, name="room"),
#     path("<str:room_name>/", views.room, name="room"),
# ]

app_name = 'chat'

router = routers.DefaultRouter()
router.register('', ChatViewSet, basename='chat')

urlpatterns = [

    # path('', include(router.urls)),
    path("", ChatViewSet.index, name="index"),
    path('room/<int:custId>/<int:mngId>/', room, name='room'),
    path('<int:user_id>/', get_names, name='user-contacts'),
    path('delete/', delete_all_chats, name='del_chats'),
    # re_path(r'room/(?P<room_name>\w+)/$', ChatConsumer.as_asgi())
]
