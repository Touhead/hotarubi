import datetime

from django.db import models
from django.utils import timezone
from PIL import Image
# Create your models here.


class GuildEvent(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateTimeField('event date')
    pub_date = models.DateTimeField('published date')
    description = models.TextField()
    short_description = models.CharField(max_length=120)
    image = models.ImageField('event image', upload_to="home/events")

    def __str__(self):
        return self.name

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=10) <= self.pub_date <= now

    def save(self, size=(1920, 1080)):

        if not self.id and not self.source:
            return

        super(GuildEvent, self).save()

        image = Image.open(self.image)

        image = image.resize(size, Image.ANTIALIAS)
        image.save(self.image.path)


class New(models.Model):
    name = models.CharField(max_length=100)
    pub_date = models.DateTimeField('published date')
    description = models.TextField()
    short_description = models.CharField(max_length=120)

    def __str__(self):
        return self.name

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=10) <= self.pub_date <= now
