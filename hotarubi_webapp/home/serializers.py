from rest_framework import serializers
from .models import GuildEvent, New, ThreadImage, PostImage, Post
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    user_post = serializers.StringRelatedField(many=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'user_post')


class GuildEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = GuildEvent


class NewSerializer(serializers.ModelSerializer):

    class Meta:
        model = New


class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    post_image = serializers.StringRelatedField(many=True)

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
