from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import MyAuthor
from django.utils.html import format_html

class UserAdmin(BaseUserAdmin):
    # Use the email field as the username field in the admin interface
    ordering = ['email']
    list_display = ['email', 'is_staff','Role','id','is_admin']
    def Role(self, obj):
        if obj.role == "customer":
            
            return format_html (f'<span style="color:blue">{obj.role}</span>')
        else:
            return format_html (f'<span style="color:green">{obj.role}</span>')
    list_filter = ['role', 'is_staff', 'email']
    fieldsets = (
        (None, {'fields': ('email', 'password','role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser','is_admin')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2','role', 'is_active', 'is_staff', 'is_superuser','is_admin')}
        ),
    )
    search_fields = ('email',)
    filter_horizontal = ()
    
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def save_model(self, request, obj, form, change):
        print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
        print(obj)
        # Hash the password before saving the user model
        obj.set_password(obj.password)
        super().save_model(request, obj, form, change)

class RestaurantManagerAdmin(admin.ModelAdmin):
    ordering = ['name']
    list_display = ['name', 'email']
    list_filter = ['name']
    search_fields = ('email', 'name')
    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def save_model(self, request, obj, form, change):
        print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
        print(obj)
        # Hash the password before saving the user model
        obj.set_password(obj.password)
        super().save_model(request, obj, form, change)
class RestaurantAdmin(admin.ModelAdmin):
    ordering = ['name','rate']
    list_display = ['name', 'manager']
    list_filter = ['rate', 'manager','name']
    search_fields = ('name',)


class CustomerAdmin(admin.ModelAdmin):
    ordering = ['name']
    list_display = ['name', 'email', 'Gender']
    list_filter = ['gender','name']
    def Gender(self, obj):
        if obj.gender == "male":
            return format_html (f'<span style="color:blue">{obj.gender}</span>')
        else:
            return format_html (f'<span style="color:purple">{obj.gender}</span>')
    search_fields = ('name','email')
    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def save_model(self, request, obj, form, change):
        print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
        print(obj)
        # Hash the password before saving the user model
        obj.set_password(obj.password)
        super().save_model(request, obj, form, change)

class VC_CodesAdmin(admin.ModelAdmin):
    ordering = ['name', 'vc_code']
    list_display = ['name', 'vc_code']
    list_filter = ['name','vc_code']
    search_fields = ('name','vc_code')

class TempManagerAdmin(admin.ModelAdmin):
    ordering = ['name']
    list_display = ['name', 'email', 'password']
    list_filter = ['email','name']

admin.site.register(Customer,CustomerAdmin)
admin.site.register(Restaurant,RestaurantAdmin)
admin.site.register(VC_Codes,VC_CodesAdmin)
admin.site.register(RestaurantManager,RestaurantManagerAdmin)
admin.site.register(MyAuthor, UserAdmin)
admin.site.register(TempManager, TempManagerAdmin)


