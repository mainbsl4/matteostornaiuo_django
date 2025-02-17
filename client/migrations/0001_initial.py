# Generated by Django 5.1.4 on 2025-02-16 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Checkin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('in_time', models.DateTimeField()),
                ('location', models.CharField(blank=True, max_length=255, null=True)),
                ('distance', models.IntegerField(blank=True, default=0, null=True)),
                ('is_approved', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Checkout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('out_time', models.DateTimeField()),
                ('status', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='CompanyProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=100)),
                ('contact_number', models.CharField(max_length=20)),
                ('company_email', models.EmailField(max_length=50)),
                ('billing_email', models.EmailField(max_length=50)),
                ('company_address', models.CharField(max_length=200)),
                ('tax_number', models.PositiveIntegerField(blank=True, null=True)),
                ('company_details', models.TextField(blank=True)),
                ('company_logo', models.ImageField(blank=True, null=True, upload_to='images/company/logo/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Company Profile',
                'verbose_name_plural': 'Company Profiles',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='FavouriteStaff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Favourite Staff',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('status', models.BooleanField(default=True)),
                ('save_template', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Job',
                'verbose_name_plural': 'Jobs',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='JobAds',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('status', models.BooleanField(default=False)),
                ('job_type', models.CharField(choices=[('full time', 'full time'), ('part time', 'part time'), ('contract', 'contract')], default='full time', max_length=20)),
                ('number_of_staff', models.IntegerField(default=1)),
                ('start_date', models.DateTimeField(db_index=True)),
                ('website_url', models.URLField(blank=True)),
                ('contact_percentage', models.IntegerField(default=0)),
                ('login_email', models.EmailField(max_length=200)),
                ('is_paid', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Permanent Job',
                'verbose_name_plural': 'Permanent Jobs',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='JobAdsJoiningRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=False)),
                ('joininig_date', models.DateTimeField(db_index=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='JobApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_approve', models.BooleanField(default=False)),
                ('in_time', models.DateTimeField(blank=True, null=True)),
                ('out_time', models.DateTimeField(blank=True, null=True)),
                ('checkin_location', models.CharField(blank=True, max_length=255, null=True)),
                ('checkout_location', models.CharField(blank=True, max_length=255, null=True)),
                ('job_status', models.CharField(choices=[('pending', 'PENDING'), ('accepted', 'ACCEPTED'), ('rejected', 'REJECTED'), ('expired', 'EXPIRED'), ('completed', 'COMPLETED')], default='pending', max_length=10)),
                ('checkin_approve', models.BooleanField(default=False)),
                ('checkout_approve', models.BooleanField(default=False)),
                ('total_working_hours', models.DurationField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='JobReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('working_hour', models.IntegerField(blank=True, null=True)),
                ('extra_hour', models.IntegerField(blank=True, null=True)),
                ('regular_pay', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('overtime_pay', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('tax', models.DecimalField(decimal_places=2, default=25, max_digits=10, null=True)),
                ('total_pay', models.DecimalField(blank=True, decimal_places=2, max_digits=50, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Job Reports',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='JobTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200)),
            ],
            options={
                'verbose_name': 'Job Template',
                'verbose_name_plural': 'Job Templates',
            },
        ),
        migrations.CreateModel(
            name='MyStaff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=False)),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'My Staff',
                'verbose_name_plural': 'My Staffs',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='StaffInvitation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='StaffReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(default=0)),
                ('message', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Staff Reviews',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Vacancy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_staff', models.IntegerField(default=1)),
                ('open_date', models.DateField()),
                ('close_date', models.DateField(blank=True)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('location', models.CharField(blank=True, max_length=255, null=True)),
                ('job_status', models.CharField(choices=[('active', 'Active'), ('progress', 'InProgress'), ('draft', 'Draft'), ('cancelled', 'Cancelled'), ('finished', 'Finished')], default='active', max_length=255)),
                ('salary', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('shift_job', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Job Vacancy',
                'verbose_name_plural': 'Job Vacancy',
                'ordering': ['-created_at'],
            },
        ),
    ]
