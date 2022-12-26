from random import randint

from django.db import models
from django.apps import apps
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import load_backend, get_backends
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, Group
# from django.core.mail import send_mail

from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField


def userDirectoryPath(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, phone=None, email=None, username=None, password=None, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username and not phone:
            raise ValueError(_('The given user must have phone number or username'))
        if phone and not username:
            username = phone
            extra_fields['is_active'] = False
        if email:
            email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name)
        username = GlobalUserModel.normalize_username(username)
        
        if 'password1' in extra_fields:
            extra_fields.pop('password1')
            extra_fields.pop('password2')
        groups = extra_fields.pop('groups')
        user_permissions = extra_fields.pop('user_permissions')

        user = self.model(username=username, email=email, phone=phone, **extra_fields)
        if user.username == user.phone:
            user.set_unusable_password()
        else:
            user.set_password(password)
        user.save(using=self._db)
        # user.groups.set(groups)
        # user.user_permissions.set(user_permissions)
        # user.save()
        return user

    def create_user(self, phone=None, email=None, username=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone=phone, email=email, username=username, password=password, **extra_fields)

    def create_superuser(self, email=None, username=None, password=None, **extra_fields):
        if not username:
            raise ValueError(_('You must provide an username'))

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self._create_user(username=username, email=email, password=password, **extra_fields)

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


class User(AbstractBaseUser, PermissionsMixin):
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
    updated = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = ['name']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
       return self.username or "No_Username"

    def save(self, *args, **kwargs):
        if self._state.adding == True: # when creating
            if self.phone and self.phone != self.username:
                self.username = self.phone
            if self.phone == self.username:
                self.is_active = False

        if self._state.adding == False: # when updating
            if self.phone and self.phone != self.username:
                self.username = self.phone
        self.full_clean()
        return super().save(*args, **kwargs)


class Profile(models.Model):
    genderChoices = (
        ('None', 'None'),
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )
    Status_Choices = (
        ('Legit', 'Legit'),
        ('Banned', 'Banned'),
    )
    membershipChoices = (
        ("Normal", "Normal"),
        ("Bronze", "Bronze"),
        ("Silver", "Silver"),
        ("Gold", "Gold"),
        ("Platinum", "Platinum"),
    )

    user = models.OneToOneField(User, on_delete=models.PROTECT, null=True, blank=True)
    name = models.CharField(_('name'), max_length=150, blank=True, null=True)
    date_of_birth = models.DateField(verbose_name=_("Date of birth"), null=True, blank=True)
    gender = models.CharField(verbose_name=_("Gender"), max_length=20, choices=genderChoices, default='None', null=True, blank=True)
    photo = models.FileField(verbose_name=_("Photo"), upload_to='photos/', default='photos/default-user-avatar.png', null=True, blank=True)
    membership = models.CharField(verbose_name=_("Membership"), max_length=50, default='Normal', choices=membershipChoices, null=True, blank=True)

    total_spend_amount = models.FloatField(verbose_name=_("Total Spend Amount"), default=0, null=True, blank=True)
    point_used = models.FloatField(verbose_name=_("Point Used"), default=0, null=True, blank=True)
    current_point = models.FloatField(verbose_name=_("Current Point"), default=0, null=True, blank=True)

    status = models.CharField(verbose_name=_("User Status"), max_length=10, default='Legit', choices=Status_Choices, null=True, blank=True)
    is_deleted = models.BooleanField(
        _('Deleted Account'),
        default=False,
        help_text=_(
            "If user deleted than this field will change to True, but reopen account won\'t change anything. "
        ),
        null=True, blank=True
    )
    created = models.DateTimeField(auto_now=True,null=True)
    updated = models.DateTimeField(auto_now_add=True,null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user",],
                name="unique_profile"
            )
        ]
    

    def __str__(self):
        if not self.user:
            return ''
        return self.user.__str__() 


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
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


class OTPtoken(models.Model):
    token_type = (
        ("Login", "Login"),
        ("Register", "Register"),
        ("PasswordReset", "PasswordReset"),
        ("Others", "Others"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(
        verbose_name=_('Type'),
        max_length=150,
        default='Login',
        choices=token_type,
        help_text=_('For which perpose this token is going to be use.'),
        null=True,
        blank=True
    )
    token = models.PositiveIntegerField(unique=True, null=True, blank=True)
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this token should be treated as active. '
            'Unselect this to make it invalidate.'
        ),
        null=True, blank=True
    )
    created = models.DateTimeField(auto_now=True,null=True)
    updated = models.DateTimeField(auto_now_add=True,null=True)

    class Meta:
        verbose_name = _('OTPToken')
        verbose_name_plural = _('OTPtokens')

    def __str__(self):
        if not self.token or not self.type:
            return 'Invalid Token'
        return f"{self.type}-{self.token}"
    
    def clean(self):
        if self._state.adding == True:
            if not self.type:
                msg = "You must provide token type"
                raise ValidationError(msg)
        if self.id == True:
            msg = "OTP Token Object is Read-Only, You can't change."
            raise ValidationError(msg)
    
    def save(self, *args, **kwargs):
        self.token = randint(100000, 999999)
        self.full_clean()
        return super().save(*args, **kwargs)




"""
# Old user methodes
    # def get_membership_type(self):
    #     if not self.Total_amount:
    #         return 'Normal'
    #     if self.Total_amount < 6000:
    #         return 'Normal'
    #     if self.Total_amount >= 6000 and self.Total_amount < 15000:
    #         return 'Bronze'
    #     elif self.Total_amount >= 15000 and self.Total_amount < 40000:
    #         return 'Silver'
    #     elif self.Total_amount >= 40000 and self.Total_amount < 60000:
    #         return 'Gold'
    #     elif self.Total_amount >= 60000:
    #         return 'Platinum'

    # def calPoint(self, Amount = 0):
    #     return round(Amount / 200, 2)

    # def save(self, *args, **kwargs):
    #     # self.Total_amount shows current value and query shows previous value
    #     # if Total_amount updated
    #     if self.pk:
    #         if self.Phone != User.objects.get(id = self.pk).Phone:
    #             self.username = f"1ds#2d54{self.Phone}df15kg2@3456gfh"
    #         if self.Total_amount or self.Total_amount == 0:
    #             previousTotal_amount = User.objects.get(id = self.pk).Total_amount
    #             if not previousTotal_amount:
    #                 previousTotal_amount = 0
    #             if self.Total_amount > previousTotal_amount:
    #                 self.Point += self.calPoint(float(self.Total_amount) - float(previousTotal_amount))
    #                 self.currentPoint += self.calPoint(float(self.Total_amount) - float(previousTotal_amount))
    #             elif self.Total_amount < previousTotal_amount:
    #                 self.Point -= self.calPoint(float(previousTotal_amount) - float(self.Total_amount))
    #                 self.currentPoint -= self.calPoint(float(previousTotal_amount) - float(self.Total_amount))
    #         else:
    #             self.Point = 0
    #     self.Membership = self.get_membership_type()
    #     super(User, self).save(*args, **kwargs)

    # def set_username(sender, instance, **kwargs):
    #     if not instance.username:
    #         instance.username = f"1ds#2d54{instance.Phone}df15kg2@3456gfh"
    # models.signals.pre_save.connect(set_username, sender=settings.AUTH_USER_MODEL)
"""
