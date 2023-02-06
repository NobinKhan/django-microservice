import django_filters

from apps.users.models import User


class UserFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = ("id", "email", "is_staff", 'username', 'phone', 'is_active')
