import datetime

from django.db import models
from django.utils import timezone
from PIL import Image
from django.contrib.auth.models import User
# Create your models here.


class Thread(models.Model):
    name = models.CharField(max_length=100)
    pub_date = models.DateTimeField('published date')
    description = models.TextField()
    short_description = models.CharField(max_length=120)

    def __str__(self):
        return self.name

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=10) <= self.pub_date <= now


class GuildEvent(Thread):
    date = models.DateTimeField('event date')


class New(Thread):
    pass


class Post(models.Model):
    user = models.ForeignKey(User, related_name='user_post')
    thread = models.ForeignKey(Thread, related_name='thread_post')
    content = models.CharField(max_length=500)

    def __str__(self):
        return self.thread.name + " - " + self.user.username + " - " + str(self.id)

class Image(models.Model):
    image = models.ImageField('event image', upload_to="home/events")

class ThreadImage(Image):
    thread = models.ForeignKey(Thread, related_name='thread_image')

    def __str__(self):
        return self.thread.name + " - " + self.image.name

class PostImage(Image):
    post = models.ForeignKey(Post, related_name='post_image')

    def __str__(self):
        return self.post.__str__() + " - " + self.image.name
