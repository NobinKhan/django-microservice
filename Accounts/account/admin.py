from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User, Profile, Address, OTPtoken
from .forms import UserCreationForm, UserChangeForm


@admin.register(User)
class UserAdminConfig(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    readonly_fields = ('date_joined', )
    ordering = ('-date_joined', )
    list_display = (
        'id',
        'username',
        'phone',
        'is_staff',
        'is_active',
    )
    list_filter = ('is_staff', 'is_superuser' )
    fieldsets = (
        ('Login Info', {
            'classes': ('collapse',),
            'fields': ('username','phone', 'password', 'is_active', 'is_staff', 'is_deleted')
        }),
        ('Personal Info', {
            'classes': ('collapse',),
            'fields': ('email',)
        }),
        ('Group Permissions', {
            'classes': ('collapse',),
            'fields': ('groups', 'user_permissions', )
        }),
        ('Important Dates', {
            'classes': ('collapse', ),
            'fields': (('date_joined',),)
        }),
    )
    add_fieldsets = (
        ('Login Info', {
            'classes': ('wide',),
            'fields': ('username', 'phone', 'password1', 'password2', 'is_active', 'is_staff'),
        }),
        ('Personal Info', {
            'classes': ('collapse',),
            'fields': ('email',)
        }),
        ('Group Permissions', {
            'classes': ('collapse',),
            'fields': ('groups', 'user_permissions', )
        }),
        ('Important Dates', {
            'classes': ('collapse', ),
            'fields': (('date_joined',),)
        }),
    )


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id','user','name', 'status', 'current_point')


@admin.register(OTPtoken)
class OTPtokenAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'token', 'created')
    list_editable = ()
    readonly_fields = ('user', 'token', 'created', 'updated')


