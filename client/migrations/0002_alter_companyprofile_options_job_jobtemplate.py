# Generated by Django 5.1.4 on 2025-01-08 10:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0001_initial'),
        ('users', '0002_skill'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='companyprofile',
            options={'verbose_name': 'Company Profile', 'verbose_name_plural': 'Company Profiles'},
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobs', to='client.companyprofile')),
            ],
        ),
        migrations.CreateModel(
            name='JobTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_title', models.CharField(max_length=200)),
                ('number_of_staff', models.IntegerField(default=1)),
                ('uniform', models.CharField(blank=True, max_length=200, null=True)),
                ('open_date', models.DateField()),
                ('close_date', models.DateField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('skills', models.ManyToManyField(blank=True, related_name='skills', to='users.skill')),
            ],
            options={
                'verbose_name': 'Job Template',
                'verbose_name_plural': 'Job Templates',
                'ordering': ['-created_at'],
            },
        ),
    ]
