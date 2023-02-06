# Generated by Django 4.1.6 on 2023-02-06 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SimpleModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RandomModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('simple_objects', models.ManyToManyField(blank=True, related_name='random_objects', to='common.simplemodel')),
            ],
        ),
        migrations.AddConstraint(
            model_name='randommodel',
            constraint=models.CheckConstraint(check=models.Q(('start_date__lt', models.F('end_date'))), name='start_date_before_end_date'),
        ),
    ]