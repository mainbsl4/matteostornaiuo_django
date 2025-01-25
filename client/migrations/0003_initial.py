

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
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='job',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobs', to='client.companyprofile'),
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
            model_name='jobtemplate',
            name='job',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.job'),
        ),
        migrations.AddField(
            model_name='jobtemplate',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='permanentjobs',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.companyprofile'),
        ),
        migrations.AddField(
            model_name='permanentjobs',
            name='skills',
            field=models.ManyToManyField(blank=True, related_name='permanent_skills', to='users.skill'),
        ),
        migrations.AddField(
            model_name='jobadsjoiningrequest',
            name='ads',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.permanentjobs'),
        ),
        migrations.AddField(
            model_name='staffinvitation',
            name='staff',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='staff.staff'),
        ),
        migrations.AddField(
            model_name='vacancy',
            name='job_title',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='users.jobrole'),
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
            model_name='vacancy',
            name='user',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='vacancies', to=settings.AUTH_USER_MODEL),
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
            model_name='job',
            name='vacancy',
            field=models.ManyToManyField(blank=True, related_name='vacancies', to='client.vacancy'),
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
    ]
