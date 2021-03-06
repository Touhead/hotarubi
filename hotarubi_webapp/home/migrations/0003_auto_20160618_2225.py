# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-18 20:25
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20160618_2150'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='content',
            field=models.CharField(default='', max_length=500),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='post',
            name='thread',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='thread_post', to='home.Thread'),
        ),
        migrations.AlterField(
            model_name='post',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_post', to=settings.AUTH_USER_MODEL),
        ),
    ]
