from typing import Any
from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin as UA
from django.core.exceptions import ValidationError
from .forms import UserCreationForm, UserChangeForm

from apps.users.services import user_create
from apps.users.models import User, Profile, Address, OTPtoken


class ProfileInline(admin.TabularInline):
    model = Profile
    fields = (
        "name",
        "status",
        "membership",
        "current_point",
        "total_spend_amount",
    )
    extra = 1


class AddressInline(admin.TabularInline):
    model = Address
    fields = (
        "name",
        "flat",
        "house",
        "address",
        "zip_code",
        "city",
    )
    extra = 1


@admin.register(User)
class UserAdmin(UA):
    form = UserChangeForm
    add_form = UserCreationForm

    ordering = ('-id', )
    inlines = (ProfileInline,)
    search_fields = ("email", "username", "phone")
    list_filter = ("is_active", "is_staff", "is_superuser")
    list_display = ("username", "phone", "is_staff", "is_superuser", "is_active", "created_at", "updated_at")
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

    def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> None:
        if change:
            return super().save_model(request, obj, form, change)

        try:
            user_create(**form.cleaned_data)
        except ValidationError as exc:
            self.message_user(request, str(exc), messages.ERROR)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id','user','name', 'status', 'current_point')


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile', 'name')


@admin.register(OTPtoken)
class OTPtokenAdmin(admin.ModelAdmin):
    list_display = ('id', 'perpose', 'token', 'created_at')
    list_editable = ()
    readonly_fields = ('user', 'token', 'created_at', 'updated_at')

