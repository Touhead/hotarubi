from rest_framework import serializers
from .models import GuildEvent, New


class EventsSerializer(serializers.ModelSerializer):

    class Meta:
        model = GuildEvent


class NewSerializer(serializers.ModelSerializer):

    class Meta:
        model = New


class NewAndGuildEventSerializer(serializers.BaseSerializer):

    def to_representation(self, obj):
        return {
            'id': obj.id,
            'name': obj.name,
            'short_description': obj.short_description,
            'type': "New" if isinstance(obj, New) else "GuildEvent"
        }