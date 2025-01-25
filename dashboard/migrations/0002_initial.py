

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('client', '0002_initial'),
        ('dashboard', '0001_initial'),
        ('staff', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='companyreview',
            name='staff',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='staff.staff'),
        ),
        migrations.AddField(
            model_name='companyreview',
            name='vacancy',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='client.vacancy'),
        ),
        migrations.AddField(
            model_name='favouritestaff',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.companyprofile'),
        ),
        migrations.AddField(
            model_name='favouritestaff',
            name='staff',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='staff.staff'),
        ),
    ]
