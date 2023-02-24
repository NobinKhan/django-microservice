from random import randint

from django.apps import apps
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import load_backend, get_backends
from django.contrib.auth.base_user import BaseUserManager as BUM
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser

from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

from apps.common.models import BaseModel


def userDirectoryPath(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'photos/profile_photo/user_{0}/{1}'.format(instance.user.id, filename)


class UserManager(BUM):
    def create_user(self, phone=None, email=None, username=None, password=None, is_active=False, is_staff=False, **extra_fields):
        extra_fields.setdefault('is_superuser', False)

        # validation
        if email:
            email = self.normalize_email(email)
        if not username:
            raise ValidationError(_('Users must have username'))

        GlobalUserModel = apps.get_model(self.model._meta.app_label, self.model._meta.object_name)
        username = GlobalUserModel.normalize_username(username)

        # creating user
        user = self.model(username=username, email=email, phone=phone, is_staff=is_staff, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.full_clean()
        user.save(using=self._db)
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
    firebase_device_id = models.CharField(max_length=1000, null=True, blank=True)
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

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = ['name']
    objects = UserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    @property
    def date_joined(self):
        return self.created_at

    def __str__(self):
       return str(self.username) or "No_Username"


class Profile(BaseModel):
    # Choices With enum functionality
    class Gender(models.TextChoices):
        NONE = 'None', _('Not Selected')
        MALE = 'Male', _('Male')
        FEMALE = 'Female', _('Female')
        OTHER = 'Other', _('Other')
    
    class AccountStatus(models.TextChoices):
        NEW = 'New', _('New Account')
        BANNED = 'Banned', _('Banned Account')

    class Membership(models.TextChoices):
        NORMAL = 'Normal'
        BRONZE = 'Bronze'
        SILVER = 'Silver'
        GOLD = 'Gold'
        PLATINUM = 'Platinum'

    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(_('name'), max_length=150, blank=True, null=True)
    date_of_birth = models.DateField(verbose_name=_("Date of birth"), null=True, blank=True)
    gender = models.CharField(verbose_name=_("Gender"), max_length=20, choices=Gender.choices, default=Gender.NONE, null=True, blank=True)
    photo = models.FileField(verbose_name=_("Photo"), upload_to=userDirectoryPath, default='photos/default-user-avatar.png', null=True, blank=True)
    membership = models.CharField(verbose_name=_("Membership"), max_length=50, default=Membership.NORMAL, choices=Membership.choices, null=True, blank=True)
    total_spend_amount = models.FloatField(verbose_name=_("Total Spend Amount"), default=0, null=True, blank=True)
    point_used = models.FloatField(verbose_name=_("Point Used"), default=0, null=True, blank=True)
    current_point = models.FloatField(verbose_name=_("Current Point"), default=0, null=True, blank=True)
    status = models.CharField(verbose_name=_("User Status"), max_length=10, default=AccountStatus.NEW, choices=AccountStatus.choices, null=True, blank=True)


    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user",],
                name="unique_profile"
            )
        ]
    
    def __str__(self):
        if not self.user:
            return _('User_Not_Found')
        return self.user.__str__() 


class Address(BaseModel):
    user = models.ForeignKey(User, related_name="addresses", on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(
        verbose_name=_('Address Name'),
        max_length=150,
        unique=True,
        help_text=_('Give a name to this address like Home or Office'),
        null=True,
        blank=True
    )
    flat =  models.CharField(verbose_name=_("Flat Number"), max_length=15, null=True, blank=True)
    house =  models.CharField(verbose_name=_("House Number"), max_length=20, null=True, blank=True)
    address = models.CharField(verbose_name=_("Address"), max_length=1024, null=True, blank=True)
    zip_code = models.CharField(verbose_name=_("Zip Code"), max_length=12, null=True, blank=True)
    city = models.CharField(verbose_name=_("City"), max_length=50, null=True, blank=True)
    country = CountryField(verbose_name=_("Country"), blank=True, null=True)
    longitude = models.CharField(max_length=250, null=True, blank=True)
    latitude = models.CharField(max_length=250, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", 'name'],
                name="unique_address"
            )
        ]

    def __str__(self):
        return self.name or 'No_Name'


class OTPtoken(BaseModel):

    class Perpose(models.TextChoices):
        OTHER = 'Other'
        LOGIN = 'Login'
        NO_USE = 'NoUse'
        REGISTER = 'Register'
        PASSWORD_RESET = 'PasswordReset'

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    perpose = models.CharField(
        verbose_name=_('Purpose of this token'),
        max_length=150,
        default=Perpose.NO_USE,
        choices=Perpose.choices,
        help_text=_('For which perpose this token is going to be use.'),
        null=True,
        blank=True
    )
    token = models.PositiveIntegerField(unique=True, null=True, blank=True)
    is_used = models.BooleanField(
        _('Is Used'),
        default=False,
        help_text=_(
            'Designates whether this token used or not. '
            'Select this to make it not usable.'
        ),
        null=True, blank=True
    )

    class Meta:
        verbose_name = _('OTPToken')
        verbose_name_plural = _('OTPtokens')

    def __str__(self):
        if not self.token or not self.perpose:
            return 'Invalid Token'
        return f"{self.perpose}-{self.token}"

    def clean(self):
        if self._state.adding == True:
            if not self.perpose:
                raise ValidationError("You must select token perpose")
            if not self.user and self.perpose != self.Perpose.OTHER:
                raise ValidationError("OTP Perpose can be only Other.")

        if self.id:
            old = OTPtoken.objects.get(pk=self.pk)
            if old.perpose != self.Perpose.OTHER and old.user:
                raise ValidationError("OTP Token Object is Read-Only, You can't change.")

    def save(self, *args, **kwargs):
        if self._state.adding == True:
            self.token = randint(100000, 999999)
        self.full_clean()
        return super().save(*args, **kwargs)

