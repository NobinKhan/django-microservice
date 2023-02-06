from django.contrib import admin, messages
from django.core.exceptions import ValidationError

from apps.users.models import User
from apps.users.services import user_create


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
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

    def save_model(self, request, obj, form, change):
        if change:
            return super().save_model(request, obj, form, change)

        try:
            print("\n *** *** *** \n")
            print(**form.cleaned_data)
            user_create(**form.cleaned_data)
        except ValidationError as exc:
            self.message_user(request, str(exc), messages.ERROR)
