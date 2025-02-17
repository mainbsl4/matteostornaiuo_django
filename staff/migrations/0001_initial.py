# Generated by Django 5.1.4 on 2025-02-16 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BankDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_holder_name', models.CharField(max_length=100)),
                ('account_number', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name_plural': 'Bank Details',
                'ordering': ['staff'],
            },
        ),
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('present', models.BooleanField(default=False)),
                ('duration', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'verbose_name_plural': 'Experience',
                'ordering': ['-start_date'],
            },
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nid_number', models.IntegerField(default=0)),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('address', models.CharField(blank=True, max_length=300)),
                ('dob', models.DateField(blank=True)),
                ('age', models.IntegerField(blank=True, null=True)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='images/staff/avatar/')),
                ('about', models.TextField(blank=True)),
                ('cv', models.FileField(blank=True, null=True, upload_to='staff/cv/')),
                ('video_cv', models.FileField(blank=True, null=True, upload_to='staff/video_resume/')),
                ('is_letme_staff', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Staff',
                'ordering': ['-created_at'],
            },
        ),
    ]
