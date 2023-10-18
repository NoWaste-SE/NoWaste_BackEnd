from django.contrib import admin
from .models import *
# Register your models here.

class FoodAdmin(admin.ModelAdmin):
    ordering = ['name']
    list_display = ['name', 'restaurant']
    list_filter = ['restaurant']
    search_fields = ['name']

class OrderAdmin(admin.ModelAdmin):
    ordering = ['created_at', 'userId']
    list_display = ['id', 'userId', 'restaurant', 'status']
    list_filter = ['status','restaurant', 'userId']
    search_fields = ('id',)

class OrderItemAdmin(admin.ModelAdmin):
    ordering = ['quantity']
    list_display = ['food', 'order']
    list_filter = ['order', 'food','quantity']
    # search_fields = (,)

class CommentAdmin(admin.ModelAdmin):
    ordering = ['created_at']
    list_display = ['writer', 'restaurant', 'created_at']
    readonly_fields = ('created_at',)
    list_filter = ['writer','restaurant']
    search_fields = ('writer',)


admin.site.register(Food,FoodAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)

admin.site.register(Comment, CommentAdmin)
