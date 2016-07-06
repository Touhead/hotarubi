from django.contrib import admin
from .models import GuildEvent, New, Post, ThreadImage, PostImage
# Register your models here.

admin.site.register(GuildEvent)
admin.site.register(New)
admin.site.register(Post)
admin.site.register(ThreadImage)
admin.site.register(PostImage)