# Generated by Django 5.1.4 on 2025-02-16 12:13

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Packages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('description', models.TextField(blank=True)),
                ('number_of_staff', models.IntegerField(default=0)),
                ('duration', models.IntegerField(default=1)),
                ('is_active', models.BooleanField(default=False)),
                ('stripe_product_id', models.CharField(blank=True, max_length=100)),
                ('stripe_price_id', models.CharField(blank=True, max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Package',
                'verbose_name_plural': 'Packages',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripe_subscriptoin_id', models.CharField(blank=True, max_length=200)),
                ('status', models.CharField(default='active', max_length=50)),
                ('start_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subscription.packages')),
            ],
        ),
    ]
