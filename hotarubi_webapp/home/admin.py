
from django.contrib import admin
from .models import GuildEvent, New, Post, ThreadImage, PostImage, EventSubscription
# Register your models here.

admin.site.register(GuildEvent)
admin.site.register(New)
admin.site.register(Post)
admin.site.register(ThreadImage)
admin.site.register(PostImage)
admin.site.register(EventSubscription)
