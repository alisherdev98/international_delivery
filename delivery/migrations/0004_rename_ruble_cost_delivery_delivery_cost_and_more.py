# Generated by Django 4.2.5 on 2023-09-19 04:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0003_delivery_session_key'),
    ]

    operations = [
        migrations.RenameField(
            model_name='delivery',
            old_name='ruble_cost',
            new_name='delivery_cost',
        ),
        migrations.AddField(
            model_name='delivery',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='delivery',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]