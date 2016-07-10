# -*- coding: utf-8 -*-

from rest_framework import serializers
from .models import GuildEvent, New, ThreadImage, PostImage, Post, Thread
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    user_post = serializers.StringRelatedField(many=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'user_post')


class ThreadSerializer(serializers.ModelSerializer):
    pub_date = serializers.DateTimeField(format=u"%Y年%m月%d日")

    class Meta:
        model = Thread


class GuildEventSerializer(serializers.ModelSerializer):
    pub_date = serializers.DateTimeField(format=u"%Y年%m月%d日")
    date = serializers.DateTimeField(format=u"%Y年%m月%d日")
    class Meta:
        model = GuildEvent


class NewSerializer(serializers.ModelSerializer):
    pub_date = serializers.DateTimeField(format=u"%Y年%m月%d日")

    class Meta:
        model = New


class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    post_image = serializers.StringRelatedField(many=True)
    pub_date = serializers.DateTimeField(format=u"%Y年%m月%d日 %H:%M")

    class Meta:
        model = Post


class NewAndGuildEventSerializer(serializers.BaseSerializer):

    def to_representation(self, obj):
        return {
            'id': obj.id,
            'name': obj.name,
            'short_description': obj.short_description,
            'type': "New" if isinstance(obj, New) else "GuildEvent"
        }


class ThreadImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ThreadImage


class PostImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostImage
