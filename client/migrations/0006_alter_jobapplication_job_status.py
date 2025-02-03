# Generated by Django 5.1.4 on 2025-02-03 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0005_alter_jobapplication_job_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobapplication',
            name='job_status',
            field=models.CharField(choices=[('PENDING', 'PENDING'), ('UPCOMMING', 'UPCOMMING'), ('ACCEPTED', 'ACCEPTED'), ('REJECTED', 'REJECTED'), ('EXPIRED', 'EXPIRED')], default='PENDING', max_length=10),
        ),
    ]
