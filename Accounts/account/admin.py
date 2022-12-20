from django.contrib import admin
from .models import User, Profile, Address
from django.contrib.auth.admin import UserAdmin


@admin.display(description='Full Name')
def full_name(obj):
    return ("%s %s" % (obj.username, obj.name))


@admin.register(User)
class UserAdminConfig(UserAdmin):
    # readonly_fields = ('username', )
    ordering = ('-date_joined', )
    list_display = (
        'id',
        'username',
        'phone',
        'is_staff',
        'is_active',
    )
    list_filter = ('phone', 'is_staff', 'is_superuser' )
    fieldsets = (
        ('Login Info', {
            'classes': ('collapse',),
            'fields': ('username','phone', 'password', 'is_active', 'is_staff')
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

