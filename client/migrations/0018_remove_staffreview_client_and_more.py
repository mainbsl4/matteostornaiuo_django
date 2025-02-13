# Generated by Django 5.1.4 on 2025-02-13 08:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0017_jobreport_staffreview'),
        ('users', '0003_remove_skill_created_at_remove_skill_updated_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='staffreview',
            name='client',
        ),
        migrations.AddField(
            model_name='staffreview',
            name='job_application',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='client.jobapplication'),
        ),
        migrations.AlterField(
            model_name='staffreview',
            name='job_role',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.jobrole'),
        ),
    ]
