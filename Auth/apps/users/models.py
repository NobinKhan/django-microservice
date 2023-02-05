from django.apps import apps
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import load_backend, get_backends
from django.contrib.auth.models import BaseUserManager as BUM
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

from apps.common.models import BaseModel

def userDirectoryPath(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class BaseUserManager(BUM):
    def create_user(self, phone=None, email=None, username=None, password=None, is_active=True, is_staff=False, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        
        if not username and not phone:
            raise ValueError(_('Users must have phone number or username'))
        if phone and not username:
            username = phone
            extra_fields['is_active'] = False
        if email:
            email = self.normalize_email(email.lower())

        GlobalUserModel = apps.get_model(self.model._meta.app_label, self.model._meta.object_name)
        username = GlobalUserModel.normalize_username(username)
            
        if 'password1' in extra_fields:
            extra_fields.pop('password1')
            extra_fields.pop('password2')
        groups = extra_fields.pop('groups')
        user_permissions = extra_fields.pop('user_permissions')

        user = self.model(username=username, email=email, phone=phone, is_active=is_active, is_staff=is_staff, **extra_fields)
        if user.username == user.phone:
            user.set_unusable_password()
        else:
            user.set_password(password)
        
        # if password is not None:
        #     user.set_password(password)
        # else:
        #     user.set_unusable_password()

        user.full_clean()
        user.save(using=self._db)

        # user.groups.set(groups)
        # user.user_permissions.set(user_permissions)
        # user.save()
        return user

    def create_superuser(self, email=None, username=None, password=None, **extra_fields):
        if not username:
            raise ValueError(_('You must provide an username'))

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True.')

        return self.create_user(username=username, email=email, password=password, **extra_fields)

    def with_perm(self, perm, is_active=True, include_superusers=True, backend=None, obj=None):
        if backend is None:
            backends = get_backends(return_tuples=True)
            if len(backends) == 1:
                backend, _ = backends[0]
            else:
                raise ValueError(
                    'You have multiple authentication backends configured and '
                    'therefore must provide the `backend` argument.'
                )
        elif not isinstance(backend, str):
            raise TypeError(
                'backend must be a dotted import path string (got %r).'
                % backend
            )
        else:
            backend = load_backend(backend)
        if hasattr(backend, 'with_perm'):
            return backend.with_perm(
                perm,
                is_active=is_active,
                include_superusers=include_superusers,
                obj=obj,
            )
        return self.none()


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.
    Username and password are required. Other fields are optional.
    """
    username_validator = UnicodeUsernameValidator()

    # User Information ######
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
        null=True,
        blank=True
    )
    password = models.CharField(_("password"), max_length=128, null=True, blank=True)
    email = models.EmailField(_('Email'), unique=True, null=True, blank=True)
    phone = PhoneNumberField(verbose_name=_("Phone"), unique=True, region='BD', blank=True, null=True)
    device_id = models.CharField(max_length=1000, null=True, blank=True)
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
        null=True, blank=True
    )
    is_deleted = models.BooleanField(
        _('Deleted Account'),
        default=False,
        help_text=_(
            'If user wants to delete account than change this field to True. '
            'If this seleted than all other objects related to this user will be marked as deleted too.'
            'If User try to reopen account than just make this false but it will not reverse other related objects. '
        ),
        null=True, blank=True
    )
    is_staff = models.BooleanField(default=False, null=True, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now=True, null=True, blank=True)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = ['name']
    objects = BaseUserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    @property
    def date_joined(self):
        return self.created_at

    def __str__(self):
       return self.username or "No_Username"




