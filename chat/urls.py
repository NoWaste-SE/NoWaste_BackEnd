# chat/urls.py
from django.urls import path

from django.urls import re_path 
from chat.consumers import ChatConsumer 

from django.urls.conf import include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from .views import *


urlpatterns = [
    path('room/<int:custId>/<int:mngId>/', room, name='room'),
    path('<int:user_id>/', get_names, name='user-contacts'),
    path('delete/', delete_all_chats, name='del_chats'),
]
