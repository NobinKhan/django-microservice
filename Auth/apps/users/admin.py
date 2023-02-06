from typing import Any
from django.contrib import admin, messages
from django.core.exceptions import ValidationError
from .forms import UserCreationForm, UserChangeForm
    

from apps.users.models import User
from apps.users.services import user_create


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # form = UserChangeForm
    add_form = UserCreationForm
    list_display = ("username", "phone", "is_staff", "is_superuser", "is_active", "created_at", "updated_at")

    search_fields = ("email", "username", "phone")

    list_filter = ("is_active", "is_staff", "is_superuser")

    fieldsets = (
        ('Login Info', {
            'classes': ('collapse',),
            'fields': ('username','phone', 'password', 'is_active', 'is_staff', 'is_deleted')
        }),
        ('Personal Info', {
            'classes': ('collapse',),
            'fields': ('email', 'firebase_device_id')
        }),
        ('Group Permissions', {
            'classes': ('collapse',),
            'fields': ('groups', 'user_permissions', )
        }),
        ('Timestamps', {
            'classes': ('collapse', ),
            'fields': (("created_at", "updated_at"),)
        }),
    )

    readonly_fields = (
        'username',
        "created_at",
        "updated_at",
        'firebase_device_id',
    )


