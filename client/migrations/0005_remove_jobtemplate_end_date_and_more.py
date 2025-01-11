# Generated by Django 5.1.4 on 2025-01-08 11:46

import datetime
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0004_job_job_template'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobtemplate',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='jobtemplate',
            name='start_date',
        ),
        migrations.AddField(
            model_name='jobtemplate',
            name='end_time',
            field=models.TimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='jobtemplate',
            name='start_time',
            field=models.TimeField(default=datetime.datetime(2025, 1, 8, 11, 46, 21, 366992, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
    ]
