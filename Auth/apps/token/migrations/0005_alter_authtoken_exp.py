# Generated by Django 4.1.7 on 2023-02-24 13:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('token', '0004_alter_authtoken_exp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authtoken',
            name='exp',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 25, 13, 13, 33, 998192, tzinfo=datetime.timezone.utc), editable=False),
        ),
    ]