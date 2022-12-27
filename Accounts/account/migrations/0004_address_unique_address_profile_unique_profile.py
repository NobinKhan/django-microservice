# Generated by Django 4.1.4 on 2022-12-24 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_remove_profile_point_remove_profile_total_paid_and_more'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='address',
            constraint=models.UniqueConstraint(fields=('user', 'name'), name='unique_address'),
        ),
        migrations.AddConstraint(
            model_name='profile',
            constraint=models.UniqueConstraint(fields=('user',), name='unique_profile'),
        ),
    ]