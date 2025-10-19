from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    ordering = ('-date_joined',)
    list_display = ('email', 'is_staff', 'is_active', 'date_joined', 'last_login')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_active','is_staff','is_superuser','groups','user_permissions')}),
        ('Important dates', {'fields': ('last_login','date_joined')}),
    )
    add_fieldsets = (
        (None, {'classes': ('wide',), 'fields': ('email','password1','password2')}),
    )
