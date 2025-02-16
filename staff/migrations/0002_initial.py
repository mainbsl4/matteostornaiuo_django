# Generated by Django 5.1.4 on 2025-02-16 09:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('staff', '0001_initial'),
        ('users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='experience',
            name='job_role',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.jobrole'),
        ),
        migrations.AddField(
            model_name='experience',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='experiences', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='staff',
            name='experience',
            field=models.ManyToManyField(blank=True, related_name='staff_experience', to='staff.experience'),
        ),
        migrations.AddField(
            model_name='staff',
            name='role',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.jobrole'),
        ),
        migrations.AddField(
            model_name='staff',
            name='skills',
            field=models.ManyToManyField(blank=True, related_name='staff_skill', to='users.skill'),
        ),
        migrations.AddField(
            model_name='staff',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='bankdetails',
            name='staff',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='staff.staff'),
        ),
    ]
