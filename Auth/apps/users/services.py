from typing import Optional

from django.db import transaction
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from phonenumber_field.phonenumber import PhoneNumber
from apps.common.services import model_update
from apps.users.models import User


def create_user(*, phone: PhoneNumber = None, username: str = None, email: str = None, is_active: bool = False, is_staff: bool = False, password: Optional[str] = None,  **extra_fields) -> User:
    # data cleaning
    if 'password1' in extra_fields:
        extra_fields.pop('password1')
        extra_fields.pop('password2')
    if 'groups' in extra_fields:
        groups = extra_fields.pop('groups')
        user_permissions = extra_fields.pop('user_permissions')
    
    # user create conditions
    if not username and not phone:
        raise ValidationError(_('Users must have phone number or username'))
    if phone and not username:
        username = phone
        is_active = False
        password = None

    # Create user
    user = User.objects.create_user(
        phone=phone,
        username=username,
        email=email, 
        is_active=is_active, 
        is_staff=is_staff, 
        password=password,
        **extra_fields
    )
    return user


@transaction.atomic
def user_update(*, user: User, data) -> User:
    non_side_effect_fields = ["first_name", "last_name"]

    user, has_updated = model_update(instance=user, fields=non_side_effect_fields, data=data)

    # Side-effect fields update here (e.g. username is generated based on first & last name)

    # ... some additional tasks with the user ...

    return user
