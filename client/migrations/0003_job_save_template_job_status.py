# Generated by Django 5.1.4 on 2025-01-13 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0002_alter_vacancy_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='save_template',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='job',
            name='status',
            field=models.CharField(default='PUBLISHED', max_length=10),
        ),
    ]
