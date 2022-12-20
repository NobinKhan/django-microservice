# Generated by Django 4.1.4 on 2022-12-20 21:32

import account.models
from django.conf import settings
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(blank=True, error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, null=True, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True, verbose_name='Email')),
                ('phone', models.CharField(blank=True, max_length=17, null=True, unique=True, validators=[django.core.validators.RegexValidator(message='Enter a valid international mobile phone number starting with +(country code)', regex='^\\+(?:[0-9]●?){6,14}[0-9]$')], verbose_name='Phone')),
                ('device_id', models.CharField(blank=True, max_length=1000, null=True)),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('is_staff', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', account.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=150, null=True, verbose_name='name')),
                ('date_of_birth', models.DateField(verbose_name='Date of birth')),
                ('gender', models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], default='Male', max_length=20, null=True, verbose_name='Gender')),
                ('photo', models.FileField(default='photos/default-user-avatar.png', upload_to='photos/', verbose_name='Photo')),
                ('membership', models.CharField(choices=[('Normal', 'Normal'), ('Bronze', 'Bronze'), ('Silver', 'Silver'), ('Gold', 'Gold'), ('Platinum', 'Platinum')], default='Normal', max_length=50)),
                ('status', models.CharField(choices=[('Normal', 'Normal'), ('Banned', 'Banned')], default='Normal', max_length=10)),
                ('total_paid', models.FloatField(blank=True, default=0, null=True)),
                ('point', models.FloatField(default=0)),
                ('point_used', models.FloatField(blank=True, default=0, null=True)),
                ('current_point', models.FloatField(blank=True, default=0, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, help_text='Give a name to this address like Home or Office', max_length=150, null=True, unique=True, verbose_name='address_name')),
                ('flat', models.CharField(blank=True, max_length=15, null=True, verbose_name='Flat Number')),
                ('house', models.CharField(blank=True, max_length=20, null=True, verbose_name='House Number')),
                ('address', models.CharField(blank=True, max_length=1024, null=True, verbose_name='Address')),
                ('zip_code', models.CharField(blank=True, max_length=12, null=True, verbose_name='Zip Code')),
                ('city', models.CharField(blank=True, max_length=50, null=True, verbose_name='City')),
                ('country', django_countries.fields.CountryField(blank=True, max_length=2, null=True, verbose_name='Country')),
                ('longitude', models.CharField(blank=True, max_length=250, null=True)),
                ('latitude', models.CharField(blank=True, max_length=250, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
