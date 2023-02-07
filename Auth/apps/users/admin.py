from typing import Any
from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin as UA
from django.core.exceptions import ValidationError
from .forms import UserCreationForm, UserChangeForm
    

from apps.users.models import User
from apps.users.services import user_create


@admin.register(User)
class UserAdmin(UA):
    form = UserChangeForm
    add_form = UserCreationForm

    ordering = ('-id', )
    search_fields = ("email", "username", "phone")
    list_display = ("username", "phone", "is_staff", "is_superuser", "is_active", "created_at", "updated_at")
    list_filter = ("is_active", "is_staff", "is_superuser")
    fieldsets = (

        ('Login Info', {
            'classes': ('wide',),
            'fields': ('username','phone', 'is_active', 'is_staff', 'is_deleted')
        }),
        ('Personal Info', {
            'classes': ('wide',),
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
    add_fieldsets = (
        ('Login Info', {
            'classes': ('wide',),
            'fields': ('username', 'phone', 'password1', 'password2', 'is_active', 'is_staff'),
        }),
        ('Personal Info', {
            'classes': ('wide',),
            'fields': ('email', 'firebase_device_id')
        }),
        # ('Group Permissions', {
        #     'classes': ('collapse',),
        #     'fields': ('groups', 'user_permissions', )
        # }),
        # ('Important Dates', {
        #     'classes': ('collapse', ),
        #     'fields': (("created_at", "updated_at"),)
        # }),
    )

    readonly_fields = (
        "created_at",
        "updated_at",
        'firebase_device_id',
    )

    def save_form(self, request: Any, form: Any, change: Any) -> Any:
        print(f"admin.py -> save_form -> before_super_call")
        forss = super().save_form(request, form, change)
        print(f"admin.py -> save_form -> after_super_call -> user_id-{forss.id}")
        return forss

    def save_model(self, request: Any, obj, form: Any, change: Any) -> None:
        print(f"admin.py -> save_model -> before_super_call -> obj-{obj} -> obj.id-{obj.id}")
        forss = super().save_model(request, obj, form, change)
        print(f"admin.py -> save_model -> after_super_call -> no_id -> user-{forss} -> type-{type(forss)}")
        return forss