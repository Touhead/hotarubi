# -*- coding: utf-8 -*-

import datetime

from django.db import models
from django.utils import timezone
from PIL import Image as PILImage
from PIL import ImageOps as PILImageOps
from django.contrib.auth.models import User
from datetime import datetime
from django.conf import settings
from io import StringIO
from django.core.files.uploadedfile import SimpleUploadedFile
import os
# Create your models here.


class Thread(models.Model):
    name = models.CharField('名', max_length=100)
    pub_date = models.DateTimeField('出版の日付')
    description = models.TextField('記述')
    short_description = models.CharField('短い記述', max_length=120)
    banner = models.ImageField('バナ－の画像(任意)', upload_to="home/threads", blank=True)

    def save(self, *args, **kwargs):
        try:
            related_img = Image.objects.get(id=self.id)
            if related_img.image != self.image:
                filename = settings.MEDIA_ROOT + self.banner.name
                img = PILImage.open(filename)
                if img.mode not in ('L', 'RGB'):
                    img = img.convert('RGB')
                img = PILImageOps.fit(img, (1920, 1080), PILImage.ANTIALIAS, 0, (0.5, 0.5)).crop((0, 200, 1920, 800))
                img.save(self.banner.path)
        except Image.DoesNotExist:
            pass
        return super(Thread, self).save()

    def __str__(self):
        return self.name

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=10) <= self.pub_date <= now

    class Meta:
        verbose_name = 'スレッド'
        verbose_name_plural = 'スレッド'


class GuildEvent(Thread):
    date = models.DateTimeField('イベントの予定の日付')


    class Meta:
        verbose_name = 'イベント'
        verbose_name_plural = 'イベント'


class New(Thread):

    class Meta:
        verbose_name = 'ニュ－ス'
        verbose_name_plural = 'ニュ－ス'


class Post(models.Model):
    user = models.ForeignKey(User, related_name='user_post', verbose_name='ユ－ザ')
    thread = models.ForeignKey(Thread, related_name='thread_post', verbose_name='スレッド')
    content = models.CharField('コメントの内容', max_length=2000)
    pub_date = models.DateTimeField('コメントの日付', default=timezone.now)

    class Meta:
        verbose_name = 'コメント'
        verbose_name_plural = 'コメント'

    def __str__(self):
        return self.thread.name + " - " + self.user.username + " - " + str(self.id)


class Image(models.Model):
    image = models.ImageField('イベントの画像', upload_to="home/threads")


class ThreadImage(Image):
    thread = models.ForeignKey(Thread, related_name='thread_image', verbose_name='ユ－ザ')

    class Meta:
        verbose_name = 'スレッドの画像'
        verbose_name_plural = 'スレッドの画像'

    def __str__(self):
        return self.thread.name + " - " + self.image.name


class PostImage(Image):
    post = models.ForeignKey(Post, related_name='post_image', verbose_name='ユ－ザ')

    class Meta:
        verbose_name = 'コメントの画像'
        verbose_name_plural = 'コメントの画像'

    def __str__(self):
        return self.post.__str__() + " - " + self.image.name
