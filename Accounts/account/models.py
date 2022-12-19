from django.db import models
from django.apps import apps
from django.contrib import auth
from django.utils import timezone
from django.core.mail import send_mail
from django_countries.fields import CountryField
from django.core.validators import RegexValidator
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager


def userDirectoryPath(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError('The given user must have email address')
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name)
        username = GlobalUserModel.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, email, username=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)

    def with_perm(self, perm, is_active=True, include_superusers=True, backend=None, obj=None):
        if backend is None:
            backends = auth._get_backends(return_tuples=True)
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
            backend = auth.load_backend(backend)
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
    email = models.EmailField(_('Email'), unique=True)
    phone_regex = RegexValidator(regex=r"^\+(?:[0-9]●?){6,14}[0-9]$", message=_("Enter a valid international mobile phone number starting with +(country code)"))
    phone = models.CharField(validators=[phone_regex], verbose_name=_("Phone"), max_length=17, blank=True, null=True)

    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['date_of_birth', 'email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = True

    # def email_user(self, subject, message, from_email=None, **kwargs):
    #     """Send an email to this user."""
    #     send_mail(subject, message, from_email, [self.email], **kwargs)





class Profile(models.Model):
    genderChoices = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )
    Status_Choices = (
        ('Normal', 'Normal'),
        ('Banned', 'Banned'),
    )
    membershipChoices = (
        ("Normal", "Normal"),
        ("Bronze", "Bronze"),
        ("Silver", "Silver"),
        ("Gold", "Gold"),
        ("Platinum", "Platinum"),
    )

    user = models.OneToOneField(User, on_delete=models.PROTECT)
    name = models.CharField(_('name'), max_length=150, blank=True, null=True)
    date_of_birth = models.DateField(verbose_name=_("Date of birth"))
    photo = models.FileField(verbose_name=_("Photo"), upload_to='photos/', default='photos/default-user-avatar.png')
    gender = models.CharField(
        verbose_name=_("Gender"),
        max_length=20,
        choices=genderChoices,
        default='Male',
        null=True,
        blank=True
    )
    permanentAddress = models.CharField(verbose_name=_(
        "Parmanent Address"), max_length=1024, null=True)
    presentAddress = models.CharField(verbose_name=_(
        "Present Address"), max_length=1024, null=True)
    # zip_code = models.CharField(verbose_name=_("Postal Code"), max_length=12)
    # city = models.CharField(verbose_name=_("City"), max_length=1024)
    # country = CountryField(blank=True, null=True)



    def __str__(self):
        if not self.user:
            return ''
        return self.user.__str__() 

# OLD Code
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.conf import settings
from django.contrib.auth.validators import UnicodeUsernameValidator





class CustomAccountManager(BaseUserManager):

    def create_superuser(self, username, email, Name, Phone, password, **other_fields):

        if not username:
            raise ValueError(_('You must provide an username'))

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        user = self.model(username=username, email=None, Name=Name, Phone=Phone, password=password, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, username, Phone, Name, **other_fields):

        if not Phone:
            raise ValueError(_('You must provide a Phone number'))

        #email = self.normalize_email(email)
        user = self.model(username=username, Phone=Phone, Name=Name, **other_fields)
        '''user.set_password(password)'''
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.
    Username and password are required. Other fields are optional.
    """
    username_validator = UnicodeUsernameValidator()
    
    genderChoices = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )
    username = models.CharField(max_length=100, unique=True, null=True, blank=True)
    email = models.EmailField(_('email address'), null=True, blank=True)
    Phone = models.CharField(max_length = 16, unique=True, null=False, blank=False)
    Device_Registration_Id = models.CharField(max_length=1000, null=True, blank=True)
    Name = models.CharField(max_length=150, null=False, blank=False)
    
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    objects = CustomAccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['Name', 'Phone', 'email']

    def __str__(self):
        return f"{self.Name} ({self.Phone})"

    def get_membership_type(self):
        if not self.Total_amount:
            return 'Normal'
        if self.Total_amount < 6000:
            return 'Normal'
        if self.Total_amount >= 6000 and self.Total_amount < 15000:
            return 'Bronze'
        elif self.Total_amount >= 15000 and self.Total_amount < 40000:
            return 'Silver'
        elif self.Total_amount >= 40000 and self.Total_amount < 60000:
            return 'Gold'
        elif self.Total_amount >= 60000:
            return 'Platinum'



    def calPoint(self, Amount = 0):
        return round(Amount / 200, 2)

    def save(self, *args, **kwargs):
        # self.Total_amount shows current value and query shows previous value
        # if Total_amount updated
        if self.pk:
            if self.Phone != User.objects.get(id = self.pk).Phone:
                self.username = f"1ds#2d54{self.Phone}df15kg2@3456gfh"
            if self.Total_amount or self.Total_amount == 0:
                previousTotal_amount = User.objects.get(id = self.pk).Total_amount
                if not previousTotal_amount:
                    previousTotal_amount = 0
                if self.Total_amount > previousTotal_amount:
                    self.Point += self.calPoint(float(self.Total_amount) - float(previousTotal_amount))
                    self.currentPoint += self.calPoint(float(self.Total_amount) - float(previousTotal_amount))
                elif self.Total_amount < previousTotal_amount:
                    self.Point -= self.calPoint(float(previousTotal_amount) - float(self.Total_amount))
                    self.currentPoint -= self.calPoint(float(previousTotal_amount) - float(self.Total_amount))
            else:
                self.Point = 0
        self.Membership = self.get_membership_type()
        super(User, self).save(*args, **kwargs)

    def set_username(sender, instance, **kwargs):
        if not instance.username:
            instance.username = f"1ds#2d54{instance.Phone}df15kg2@3456gfh"
    models.signals.pre_save.connect(set_username, sender=settings.AUTH_USER_MODEL)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=250, null=True, blank=True)
    appartment =  models.CharField(max_length=250, null=True, blank=True)
    house =  models.CharField(max_length=250, null=True, blank=True)
    longitude = models.CharField(max_length=250, null=True, blank=True)
    latitude = models.CharField(max_length=250, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=20, decimal_places=2, default=0, null=True, blank=True) # Default added for testing
    status = models.CharField(max_length=10, default='Normal', choices=Status_Choices)
    discount = models.PositiveIntegerField(null=True,blank=True)
    membership = models.CharField(max_length=50, default='Normal', choices=membershipChoices)
    point = models.FloatField(default=0)
    used_point = models.FloatField(default=0, null=True, blank=True)
    current_point = models.FloatField(default=0, null=True, blank=True)
