# Generated by Django 4.1.7 on 2023-02-19 17:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('token', '0003_authtoken_jti_alter_authtoken_exp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authtoken',
            name='exp',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 20, 17, 23, 30, 752122, tzinfo=datetime.timezone.utc), editable=False),
        ),
    ]