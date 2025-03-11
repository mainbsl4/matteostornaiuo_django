# Generated by Django 5.1.4 on 2025-03-11 06:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('client', '0002_initial'),
        ('staff', '0001_initial'),
        ('users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='companyprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profiles', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='companyreview',
            name='review_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='staff.staff'),
        ),
        migrations.AddField(
            model_name='companyreview',
            name='review_for',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='client.companyprofile'),
        ),
        migrations.AddField(
            model_name='favouritestaff',
            name='company',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='client.companyprofile'),
        ),
        migrations.AddField(
            model_name='favouritestaff',
            name='staff',
            field=models.ManyToManyField(blank=True, related_name='favourites_staff', to='staff.staff'),
        ),
        migrations.AddField(
            model_name='job',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobs', to='client.companyprofile'),
        ),
        migrations.AddField(
            model_name='jobads',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.companyprofile'),
        ),
        migrations.AddField(
            model_name='jobads',
            name='skills',
            field=models.ManyToManyField(blank=True, related_name='permanent_skills', to='users.skill'),
        ),
        migrations.AddField(
            model_name='jobadsjoiningrequest',
            name='ads',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.jobads'),
        ),
        migrations.AddField(
            model_name='jobadsjoiningrequest',
            name='staff',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='staff.staff'),
        ),
        migrations.AddField(
            model_name='jobapplication',
            name='applicant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='staff.staff'),
        ),
        migrations.AddField(
            model_name='jobreport',
            name='job_application',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='client.jobapplication'),
        ),
        migrations.AddField(
            model_name='jobtemplate',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.companyprofile'),
        ),
        migrations.AddField(
            model_name='jobtemplate',
            name='job',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.job'),
        ),
        migrations.AddField(
            model_name='mystaff',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.companyprofile'),
        ),
        migrations.AddField(
            model_name='mystaff',
            name='staff',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='staff.staff'),
        ),
        migrations.AddField(
            model_name='staffinvitation',
            name='staff',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='staff.staff'),
        ),
        migrations.AddField(
            model_name='vacancy',
            name='job',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vacancies', to='client.job'),
        ),
        migrations.AddField(
            model_name='vacancy',
            name='job_title',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.jobrole'),
        ),
        migrations.AddField(
            model_name='vacancy',
            name='participants',
            field=models.ManyToManyField(blank=True, related_name='participants', to='staff.staff'),
        ),
        migrations.AddField(
            model_name='vacancy',
            name='skills',
            field=models.ManyToManyField(blank=True, related_name='skills', to='users.skill'),
        ),
        migrations.AddField(
            model_name='vacancy',
            name='uniform',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.uniform'),
        ),
        migrations.AddField(
            model_name='staffinvitation',
            name='vacancy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.vacancy'),
        ),
        migrations.AddField(
            model_name='jobapplication',
            name='vacancy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.vacancy'),
        ),
        migrations.AddField(
            model_name='checkout',
            name='vacancy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.vacancy'),
        ),
        migrations.AddField(
            model_name='checkin',
            name='vacancy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.vacancy'),
        ),
        migrations.AddIndex(
            model_name='vacancy',
            index=models.Index(fields=['open_date', 'close_date', 'start_time', 'end_time'], name='client_vaca_open_da_48c6cf_idx'),
        ),
    ]
