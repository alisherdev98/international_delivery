# Generated by Django 4.2.5 on 2023-09-18 07:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sessions', '0001_initial'),
        ('delivery', '0002_remove_delivery_dollar_cost_delivery_content_cost_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='delivery',
            name='session_key',
            field=models.ForeignKey(default='e58hniutp6udlrx0t7dxxh69srdlm06y', on_delete=django.db.models.deletion.PROTECT, to='sessions.session', verbose_name='ключ сессии клиента'),
            preserve_default=False,
        ),
    ]
