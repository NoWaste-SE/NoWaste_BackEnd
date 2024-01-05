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
    list_display = ['id', 'userId', 'restaurant', 'status','cart']
    list_filter = ['status','restaurant', 'userId','cart']
    search_fields = ('id','cart')

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

class CartAdmin(admin.ModelAdmin):
    ordering = ['user']
    list_display = ['user']
    list_filter = ['user']
    search_fields = ('user',)

admin.site.register(Food,FoodAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)

admin.site.register(Comment, CommentAdmin)

admin.site.register(Order2)
admin.site.register(OrderItem2)
admin.site.register(RecentlyViewedRestaurant)
admin.site.register(Cart,CartAdmin)
# admin.site.register(OrderManager)
# admin.site.register(OrderItemManager)
