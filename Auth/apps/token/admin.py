from django.contrib import admin

from apps.token.models import RsaKey


@admin.register(RsaKey)
class RsaKeyAdmin(admin.ModelAdmin):
    list_display = ('id', 'active', 'created_at', 'updated_at')
    list_editable = ()
    readonly_fields = ('public', 'private', 'active', 'created_at', 'updated_at')

