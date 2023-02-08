# Generated by Django 4.1.6 on 2023-02-08 05:41

import apps.users.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_user_first_name_remove_user_last_name'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
            ],
        ),
        migrations.RemoveConstraint(
            model_name='address',
            name='unique_address',
        ),
        migrations.RemoveField(
            model_name='address',
            name='profile',
        ),
        migrations.AddField(
            model_name='address',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.FileField(blank=True, default='photos/default-user-avatar.png', null=True, upload_to=apps.users.models.userDirectoryPath, verbose_name='Photo'),
        ),
        migrations.AddConstraint(
            model_name='address',
            constraint=models.UniqueConstraint(fields=('user', 'name'), name='unique_address'),
        ),
    ]
