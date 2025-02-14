# Generated by Django 5.1.6 on 2025-02-13 23:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('finance', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purchased_at', models.DateField()),
                ('count', models.DecimalField(decimal_places=10, max_digits=20)),
                ('spent', models.DecimalField(decimal_places=2, max_digits=15)),
                ('cost_for_one', models.DecimalField(decimal_places=6, max_digits=15)),
                ('action', models.CharField(choices=[('+', 'Buy'), ('-', 'Sell')], max_length=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('coin', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='finance.coin')),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='finance.currency')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
