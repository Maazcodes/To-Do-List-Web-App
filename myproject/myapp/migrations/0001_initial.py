# Generated by Django 3.2 on 2021-07-27 17:42

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyTasks',
            fields=[
                ('task_id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('task_title', models.CharField(default='', help_text='The title of the task', max_length=100, verbose_name='Task Title')),
                ('task_desc', models.TextField(default='', help_text='The description of task', verbose_name='Task Description')),
                ('task_time', models.DateTimeField(default=datetime.datetime(2021, 7, 27, 17, 42, 17, 573771, tzinfo=utc))),
            ],
        ),
    ]
