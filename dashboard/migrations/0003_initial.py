

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('client', '0003_initial'),
        ('dashboard', '0002_initial'),
        ('staff', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='staffreview',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.companyprofile'),
        ),
        migrations.AddField(
            model_name='staffreview',
            name='staff',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='staff.staff'),
        ),
        migrations.AddField(
            model_name='staffreview',
            name='vacancy',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='client.vacancy'),
        ),
    ]
