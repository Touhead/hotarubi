# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-13 19:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_auto_20160710_1556'),
    ]

    operations = [
        migrations.AddField(
            model_name='thread',
            name='banner_original',
            field=models.ImageField(blank=True, upload_to='home/threads', verbose_name='バナ－の画像(任意)'),
        ),
        migrations.AlterField(
            model_name='thread',
            name='banner',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]
