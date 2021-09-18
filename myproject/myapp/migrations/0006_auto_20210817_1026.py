# Generated by Django 3.2.6 on 2021-08-17 10:26

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myapp', '0005_auto_20210817_0957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mytasks',
            name='task_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 17, 10, 26, 47, 819545, tzinfo=utc), verbose_name='Task Date & Time'),
        ),
        migrations.AlterField(
            model_name='mytasks',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mytasks', to=settings.AUTH_USER_MODEL),
        ),
    ]
