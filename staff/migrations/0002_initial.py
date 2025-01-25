

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('staff', '0001_initial'),
        ('users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='skills',
            field=models.ManyToManyField(blank=True, related_name='staff_skill', to='users.skill'),
        ),
        migrations.AddField(
            model_name='staff',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='staffrole',
            name='role',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.jobrole'),
        ),
        migrations.AddField(
            model_name='staffrole',
            name='staff',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='staff.staff'),
        ),
    ]
