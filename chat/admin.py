from django.contrib import admin
from django.core.paginator import *
from django.core.cache import cache
from django.db import models
from .models import *


class ChatAdmin(admin.ModelAdmin):
    ordering = ['date_created']
    list_display = ['room_name', 'sender_id', 'date_created']
    list_filter = ['sender_id','room_name']
    search_fields = ('room_name',)
admin.site.register(Chat, ChatAdmin)

class RoomAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ['room_name', 'customer', 'manager']
    list_filter = ['customer','manager','room_name']
    search_fields = ('room_name','customer','manager')
admin.site.register(Room, RoomAdmin)
