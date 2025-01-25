
# Generated by Django 5.1.4 on 2025-01-25 05:41


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
                ('status', models.BooleanField(default=False)),
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
                ('company_details', models.TextField(blank=True)),
                ('company_logo', models.ImageField(blank=True, null=True, upload_to='images/company/logo/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Company Profile',
                'verbose_name_plural': 'Company Profiles',
            },
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('status', models.CharField(default='PUBLISHED', max_length=10)),
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
                ('status', models.BooleanField(default=False)),
                ('in_time', models.DateTimeField(blank=True, null=True)),
                ('out_time', models.DateTimeField(blank=True, null=True)),
                ('job_status', models.CharField(choices=[('UPCOMMING', 'UPCOMMING'), ('ACCEPTED', 'ACCEPTED'), ('REJECTED', 'REJECTED'), ('EXPIRED', 'EXPIRED')], default='UPCOMMING', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='JobTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='PermanentJobs',
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
            name='StaffInvitation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Vacancy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_staff', models.IntegerField(default=1)),
                ('open_date', models.DateField()),
                ('close_date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('salary', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
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
